from xml.etree.ElementTree import fromstring

from fastapi import FastAPI, Depends, HTTPException
from requests import Session as request_session
from sqlalchemy.orm import Session as sql_session
from zeep import Transport, Client

from src import models
from src.database import SessionLocal
from src.models import Company
from src.schemas import Company as company_schema

app = FastAPI()

SANDBOX_URL = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-test.wsdl'
SANDBOX_PASSWORD = 'abcde12345abcde12345'


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_formatted_data(data):
    return {info.tag: "" if info.text is None else info.text for info in fromstring(data)[0]}


def get_company_by_nip(nip):
    headers = {}
    transport = Transport(session=request_session())
    transport.session.headers = headers
    client = Client(SANDBOX_URL, transport=transport)
    session_key = client.service.Zaloguj(
        pKluczUzytkownika=SANDBOX_PASSWORD
    )
    headers.update({"sid": session_key})
    data = client.service.DaneSzukajPodmioty(pParametryWyszukiwania={'Nip': nip})
    client.service.Wyloguj(pIdentyfikatorSesji=session_key)
    return get_formatted_data(data)


@app.get("/{nip}")
async def get_company_regon_api(nip: int):
    return get_company_by_nip(nip)


@app.post("/create/{nip}")
async def create_company(nip: int, db: sql_session = Depends(get_db)):
    company_data = get_company_by_nip(nip)
    db_company = Company(nip=company_data.get("Nip"), regon=company_data.get("Regon"),
                         name=company_data.get("Nazwa"))
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@app.put("/update/{company_id}")
async def update_company(company_id: int, company: company_schema, db: sql_session = Depends(get_db)):
    company_model = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company_model:
        raise http_exception()
    company_model.nip = company.nip
    company_model.regon = company.regon
    company_model.name = company.name

    db.add(company_model)
    db.commit()

    return successful_response(200)


@app.delete("/delete/{company_id")
async def delete_company(company_id: int, db: sql_session = Depends(get_db)):
    company_model = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company_model:
        raise http_exception()
    db.query(models.Company).filter(models.Company.id == company_id).delete()
    db.commit()
    return successful_response(200)


@app.get("/companies/")
async def get_all_companies(db: sql_session = Depends(get_db)):
    return db.query(models.Company).all()


@app.get("/companies/{nip}")
async def get__company(nip: int, db: sql_session = Depends(get_db)):
    return db.query(models.Company).filter(models.Company.nip == nip).first()


def successful_response(status_code: int):
    return {'status': status_code, 'transaction': 'Successful'}


def http_exception():
    return HTTPException(status_code=404, detail="Item not found")

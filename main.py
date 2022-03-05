from xml.etree.ElementTree import fromstring

from fastapi import FastAPI, Depends
from requests import Session as request_session
from sqlalchemy.orm import Session as sql_session
from zeep import Transport, Client

from src.database import SessionLocal
from src.models import Company

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
async def get_company(nip: int):
    return get_company_by_nip(nip)


@app.get("/create/{nip}")
async def create_company(nip: int, db: sql_session = Depends(get_db)):
    company_data = get_company_by_nip(nip)
    db_company = Company(nip=company_data.get("Nip"), regon=company_data.get("Regon"),
                         name=company_data.get("Nazwa"))
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

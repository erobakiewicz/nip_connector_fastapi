from fastapi import FastAPI
from requests import Session
from zeep import Transport, Client

app = FastAPI()


SANDBOX_URL = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-test.wsdl'
SANDBOX_PASSWORD = 'abcde12345abcde12345'


@app.get("/{nip}")
async def get_nip(nip: int):
    headers = {}
    transport = Transport(session=Session())
    transport.session.headers = headers
    client = Client(SANDBOX_URL, transport=transport)
    session_key = client.service.Zaloguj(
        pKluczUzytkownika=SANDBOX_PASSWORD
    )
    headers.update({"sid": session_key})
    data = client.service.DaneSzukajPodmioty(pParametryWyszukiwania={'Nip': nip})
    client.service.Wyloguj(pIdentyfikatorSesji=session_key)
    return data


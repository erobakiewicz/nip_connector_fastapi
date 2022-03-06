from sqlalchemy import Column, Integer, String, BigInteger

from src.database import Base


class Company(Base):
    __tablename__ = "comapnies"

    id = Column(Integer, primary_key=True, index=True)
    nip = Column(BigInteger)
    regon = Column(BigInteger)
    name = Column(String)

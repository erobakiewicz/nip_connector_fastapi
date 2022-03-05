from sqlalchemy import Column, Integer, String

from src.database import Base


class Company(Base):
    __tablename__ = "comapnies"

    id = Column(Integer, primary_key=True, index=True)
    nip = Column(String)
    regon = Column(String)
    name = Column(String)

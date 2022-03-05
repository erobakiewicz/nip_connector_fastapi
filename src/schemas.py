from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    id: int
    nip: Optional[str] = None
    regon: Optional[str] = None
    name: Optional[str] = None

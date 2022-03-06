from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    id: int
    nip: int
    regon: int
    name: Optional[str] = None

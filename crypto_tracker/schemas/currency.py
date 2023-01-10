from pydantic import BaseModel
from typing import Optional

class CurrencyBase(BaseModel):
    name: str
    symbol: str
    image_url: str


class CurrencyCreate(CurrencyBase):
    ...


class Currency(CurrencyBase):
    id: int
    price: Optional[float] = None

    class Config:
        orm_mode = True
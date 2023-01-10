from datetime import date
from pydantic import BaseModel


class Candlestick(BaseModel):
    date: date
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float

    class Config:
        orm_mode = True
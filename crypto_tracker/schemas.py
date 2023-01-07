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


class CurrencyBase(BaseModel):
    name: str
    symbol: str
    image_url: str


class CurrencyCreate(CurrencyBase):
    ...


class Currency(CurrencyBase):
    id: int
    price: float | None = None

    class Config:
        orm_mode = True


class PortfolioBase(BaseModel):
    title: str
    currency_id: int
    amount: float


class PortfolioCreate(PortfolioBase):
    ...


class PortfolioUpdate(BaseModel):
    id: int
    amount: float


class Portfolio(PortfolioBase):
    id: int
    user_id: int
    currency: Currency = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    portfolio: list[Portfolio] = []
    
    class Config:
        orm_mode = True


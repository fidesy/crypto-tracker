from pydantic import BaseModel

from .currency import Currency


class AssetBase(BaseModel):
    currency_id: int
    amount: float


class AssetCreate(AssetBase):
    ...


class AssetUpdate(AssetCreate):
    id: int


class Asset(AssetBase):
    id: int
    portfolio_id: int
    currency: Currency = None

    class Config:
        orm_mode = True
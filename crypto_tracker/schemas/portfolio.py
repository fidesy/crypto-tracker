from pydantic import BaseModel

from .asset import Asset


class PortfolioBase(BaseModel):
    title: str


class PortfolioCreate(PortfolioBase):
    ...


class Portfolio(PortfolioBase):
    id: int
    assets: list[Asset] = None

    class Config:
        orm_mode = True
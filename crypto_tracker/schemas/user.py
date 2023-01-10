from pydantic import BaseModel

from .portfolio import Portfolio


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    portfolios: list[Portfolio] = []
    
    class Config:
        orm_mode = True
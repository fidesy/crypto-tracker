from sqlalchemy import Column, Date, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from .database import Base


class Candlestick(Base):
    __tablename__ = "candlesticks"

    date = Column(Date, primary_key=True)
    symbol = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    symbol = Column(String)
    image_url = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    portfolio = relationship("Portfolio", back_populates="user")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    
    user = relationship("User", back_populates="portfolio")
    currency = relationship("Currency")
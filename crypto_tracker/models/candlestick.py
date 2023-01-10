from sqlalchemy import Column, Date, Float, String

from ..database import Base


class Candlestick(Base):
    __tablename__ = "candlesticks"

    date = Column(Date, primary_key=True)
    symbol = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

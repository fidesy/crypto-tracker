from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    amount = Column(Float)

    currency = relationship("Currency")
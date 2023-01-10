from sqlalchemy import Column, Integer, String

from ..database import Base


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    symbol = Column(String)
    image_url = Column(String)
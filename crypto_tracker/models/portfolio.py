from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from ..database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    assets = relationship("Asset")
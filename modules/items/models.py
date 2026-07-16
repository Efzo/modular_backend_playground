from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description =  Column(String, nullable=True)
    price = Column(Float, nullable=False)
    buyer = Column(String, nullable=False)
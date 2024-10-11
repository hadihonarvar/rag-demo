# create sql alchemy models for product
# create qdrant collection for product
import uuid
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Text, UUID, Float
from sqlalchemy.orm import relationship
from app.databases.psql_db import Base


class Product(Base):
    __tablename__ = 'products'
        
    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    # reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    # assets = relationship("Asset", back_populates="product", cascade="all, delete-orphan")
    # store_id = Column(Integer, ForeignKey('stores.id'))
    # store = relationship("Store", back_populates="products")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "rating": self.rating
        }
    
    

class ProductPoint(BaseModel):
    id: uuid.UUID
    vector: List[float]
    payload: dict

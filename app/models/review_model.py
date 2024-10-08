import uuid
from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    
    product = relationship("Product", back_populates="reviews")
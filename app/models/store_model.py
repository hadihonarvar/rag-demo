# import uuid
# from typing import List
# from pydantic import BaseModel
# from sqlalchemy import Column, ForeignKey, Integer, String, Text
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base


# Base = declarative_base()

# class Store(Base):
#     __tablename__ = "stores"
#     id = Column(Integer, primary_key=True, index=True)

#     name = Column(String(255), nullable=False, unique=True)
#     url: Column(String(255), nullable=False, unique=True)
#     products = relationship("Product", back_populates="store", cascade="all, delete-orphan")

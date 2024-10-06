# create sql alchemy models for product
# create qdrant collection for product
import uuid
from typing import List
from pydantic import BaseModel
from app import db


class Product(BaseModel):
    id: uuid
    name: str
    title: str
    description: str
    price: float
    assets: List[str]
    reviews: List[str]
    rating: float
    store: uuid

class ProductPoint(BaseModel):
    id: uuid
    vector: List[float]
    payload: dict


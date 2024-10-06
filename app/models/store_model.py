import uuid
from typing import List
from pydantic import BaseModel
from app import db

class Store(BaseModel):
    name: str
    url: str
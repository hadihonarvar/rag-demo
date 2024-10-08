import uuid
from typing import List, Optional
from pydantic import BaseModel, UUID4



class ProductDTO(BaseModel):
    id: Optional[UUID4] = uuid.uuid4()
    name: str
    title: str
    description: str
    price: float
    assets: List[str]
    reviews: List[str]
    rating: float
    store: uuid.UUID
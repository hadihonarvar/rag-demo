import uuid
from typing import List, Optional
from pydantic import BaseModel, UUID4

class ProductDTO(BaseModel):
    id: Optional[UUID4] = None 
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    # assets: Optional[List[str]] = None
    # reviews: Optional[List[str]] = None
    # store: Optional[UUID4] = None 

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = uuid.uuid4()

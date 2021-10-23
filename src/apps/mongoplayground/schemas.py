from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional


class Book(BaseModel):
    pk: int
    title:  Optional[str] = None
    author_id: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[int] = None
class Product(BaseModel):
    title:  Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = 0
    image: Optional[str] = None
    shop : Optional[str] = None
    
    
class Shop(BaseModel):
    name : Optional[str] = None
    started_before: Optional[int] = 0
    displayPicture : Optional[str] = None
    owner : Optional[str] = None   
    

# class Book(BaseModel):
#     topic: str
#     args: List[inner_data]

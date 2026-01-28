from typing import List, Optional
from pydantic import BaseModel
from src.domain.entities.item import ItemType

class ItemCreateDTO(BaseModel):
    name: str
    type: ItemType
    description: str
    price: int = 0

class ItemUpdateDTO(BaseModel):
    name: Optional[str] = None
    type: Optional[ItemType] = None
    description: Optional[str] = None
    price: Optional[int] = None

class ItemResponseDTO(BaseModel):
    id: int
    name: str
    type: str
    description: str
    price: int
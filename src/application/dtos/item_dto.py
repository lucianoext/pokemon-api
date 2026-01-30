from pydantic import BaseModel
from src.domain.entities.item import ItemType

class ItemCreateDTO(BaseModel):
    name: str
    type: ItemType
    description: str
    price: int = 0

class ItemUpdateDTO(BaseModel):
    name: str | None = None
    type: ItemType | None = None
    description: str | None = None
    price:  int | None = None

class ItemResponseDTO(BaseModel):
    id: int
    name: str
    type: str
    description: str
    price: int
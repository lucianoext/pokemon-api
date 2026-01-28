from typing import List, Optional
from pydantic import BaseModel

class BackpackAddItemDTO(BaseModel):
    trainer_id: int
    item_id: int
    quantity: int = 1

class BackpackRemoveItemDTO(BaseModel):
    quantity: int = 1

class BackpackUpdateQuantityDTO(BaseModel):
    new_quantity: int

class BackpackItemResponseDTO(BaseModel):
    id: int
    trainer_id: int
    item_id: int
    item_name: str
    item_type: str
    item_description: str
    item_price: int
    quantity: int

class BackpackResponseDTO(BaseModel):
    trainer_id: int
    trainer_name: str
    total_items: int
    items: List[BackpackItemResponseDTO]
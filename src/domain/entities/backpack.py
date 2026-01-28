from typing import Optional
from dataclasses import dataclass

@dataclass
class Backpack:
    id: Optional[int]
    trainer_id: int
    item_id: int
    quantity: int
    
    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
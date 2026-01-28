from typing import Optional
from dataclasses import dataclass
from enum import Enum

class ItemType(Enum):
    POKEBALL = "pokeball"
    ANTIDOTE = "antidote"
    BERRY = "berry"
    POTION = "potion"
    REVIVE = "revive"
    STONE = "stone"
    TM = "tm"

@dataclass
class Item:
    id: Optional[int]
    name: str
    type: ItemType
    description: str
    price: int = 0
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = ItemType(self.type)
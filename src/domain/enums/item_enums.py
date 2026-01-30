from enum import Enum

class ItemType(str, Enum):
    POKEBALL = "pokeball"
    ANTIDOTE = "antidote"
    BERRY = "berry"
    POTION = "potion"
    REVIVE = "revive"
    STONE = "stone"
    TM = "tm"
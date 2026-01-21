from typing import Optional
from dataclasses import dataclass
from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Region(Enum):
    KANTO = "kanto"
    JOHTO = "johto"
    HOENN = "hoenn"
    SINNOH = "sinnoh"
    UNOVA = "unova"
    KALOS = "kalos"
    ALOLA = "alola"
    GALAR = "galar"

@dataclass
class Trainer:
    id: Optional[int]
    name: str
    gender: Gender
    region: Region
    
    def __post_init__(self):
        if isinstance(self.gender, str):
            self.gender = Gender(self.gender)
        if isinstance(self.region, str):
            self.region = Region(self.region)
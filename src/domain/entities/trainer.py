from typing import Optional      # Como Nullable<T> en C#
from dataclasses import dataclass # Como record en C# 11
from enum import Enum            # Como enum en C#

class Gender(Enum):
    MALE = "male"
    FEMALE = "female" 
    OTHER = "other"

class Region(Enum):
    KANTO = "kanto"
    JOHTO = "johto"
    HOENN = "hoenn"

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
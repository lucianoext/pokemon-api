from typing import List, Optional
from pydantic import BaseModel

from src.domain.entities.pokemon import PokemonNature, PokemonType


class PokemonCreateDTO(BaseModel):
    name: str
    type_primary: PokemonType
    type_secondary: Optional[PokemonType] = None
    attacks: List[str]
    nature: PokemonNature
    level: int = 1

class PokemonUpdateDTO(BaseModel):
    name: Optional[str] = None
    type_primary: Optional[PokemonType] = None
    type_secondary: Optional[PokemonType] = None
    attacks: Optional[List[str]] = None
    nature: Optional[PokemonNature] = None
    level: Optional[int] = None

class PokemonResponseDTO(BaseModel):
    id: int
    name: str
    type_primary: str        
    type_secondary: Optional[str] = None
    attacks: List[str]
    nature: str
    level: int
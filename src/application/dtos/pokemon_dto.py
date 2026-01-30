from pydantic import BaseModel

from src.domain.entities.pokemon import PokemonNature, PokemonType


class PokemonCreateDTO(BaseModel):
    name: str
    type_primary: PokemonType
    type_secondary: PokemonType | None = None
    attacks: list[str]
    nature: PokemonNature
    level: int = 1

class PokemonUpdateDTO(BaseModel):
    name: str | None = None
    type_primary: PokemonType | None = None
    type_secondary: PokemonType | None = None
    attacks: list[str] | None = None
    nature: PokemonNature | None = None
    level:  int | None = None

class PokemonResponseDTO(BaseModel):
    id: int
    name: str
    type_primary: str        
    type_secondary: str | None = None
    attacks: list[str]
    nature: str
    level: int
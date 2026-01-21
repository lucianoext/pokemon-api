from pydantic import BaseModel
from typing import Optional, List
from src.domain.entities.trainer import Gender, Region

class TrainerCreateDTO(BaseModel):
    name: str
    gender: Gender
    region: Region
    
    class Config:
        use_enum_values = True

class TrainerUpdateDTO(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    region: Optional[Region] = None
    
    class Config:
        use_enum_values = True

class PokemonSummaryDTO(BaseModel):
    id: int
    name: str
    type_primary: str
    level: int

class TrainerResponseDTO(BaseModel):
    id: int
    name: str
    gender: str
    region: str
    team_size: int
    pokemon_team: List[PokemonSummaryDTO] = []
    
    class Config:
        from_attributes = True
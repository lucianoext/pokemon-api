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

class TrainerResponseDTO(BaseModel):
    id: int
    name: str
    gender: str
    region: str
    team_size: int
    
    class Config:
        from_attributes = True
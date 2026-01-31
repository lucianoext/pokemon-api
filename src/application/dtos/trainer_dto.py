from pydantic import BaseModel

from src.domain.entities.trainer import Gender, Region


class TrainerCreateDTO(BaseModel):
    name: str
    gender: Gender
    region: Region

    class Config:
        use_enum_values = True


class TrainerUpdateDTO(BaseModel):
    name: str | None = None
    gender: Gender | None = None
    region: Region | None = None

    class Config:
        use_enum_values = True


class PokemonSummaryDTO(BaseModel):
    id: int
    name: str
    type_primary: str
    level: int


class TrainerResponseDTO(BaseModel):
    id: int | None
    name: str
    gender: str
    region: str
    team_size: int
    pokemon_team: list[PokemonSummaryDTO] = []

    class Config:
        from_attributes = True

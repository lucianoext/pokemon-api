from pydantic import BaseModel

class TeamAddPokemonDTO(BaseModel):
    trainer_id: int
    pokemon_id: int
    position: int

class TeamUpdatePositionDTO(BaseModel):
    new_position: int

class TeamMemberResponseDTO(BaseModel):
    id: int
    trainer_id: int
    pokemon_id: int
    pokemon_name: str
    pokemon_type: str
    pokemon_level: int
    position: int
    is_active: bool

class TeamResponseDTO(BaseModel):
    trainer_id: int
    trainer_name: str
    team_size: int
    max_size: int = 6
    members: list[TeamMemberResponseDTO]
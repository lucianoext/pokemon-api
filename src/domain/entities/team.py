from dataclasses import dataclass

@dataclass
class Team:
    id:  int | None
    trainer_id: int
    pokemon_id: int
    position: int
    is_active: bool = True
    
    def __post_init__(self):
        if self.position < 1 or self.position > 6:
            raise ValueError("Position must be between 1 and 6")
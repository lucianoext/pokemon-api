from abc import ABC, abstractmethod
from ..entities.team import Team

class TeamRepository(ABC):
    
    @abstractmethod
    def add_pokemon_to_team(self, team: Team) -> Team:
        pass
    
    @abstractmethod
    def remove_pokemon_from_team(self, trainer_id: int, pokemon_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_team_by_trainer(self, trainer_id: int) -> list[Team]:
        pass
    
    @abstractmethod
    def get_team_member(self, trainer_id: int, pokemon_id: int) -> Team | None:
        pass
    
    @abstractmethod
    def update_position(self, trainer_id: int, pokemon_id: int, new_position: int) -> Team | None:
        pass
    
    @abstractmethod
    def get_trainer_team_size(self, trainer_id: int) -> int:
        pass
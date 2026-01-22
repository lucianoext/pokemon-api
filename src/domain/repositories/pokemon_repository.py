from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.pokemon import Pokemon


class PokemonRepository(ABC):
    
    @abstractmethod
    def create(self, pokemon: Pokemon) -> Pokemon:
        pass
    
    @abstractmethod
    def get_by_id(self, pokemon_id: int) -> Optional[Pokemon]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pokemon]:
        pass
    
    @abstractmethod
    def update(self, pokemon_id: int, trainer: Pokemon) -> Optional[Pokemon]:
        pass
    
    @abstractmethod
    def delete(self, pokemon_id: int) -> bool:
        pass
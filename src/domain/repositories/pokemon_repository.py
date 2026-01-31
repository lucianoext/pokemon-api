from abc import ABC, abstractmethod

from ..entities.pokemon import Pokemon


class PokemonRepository(ABC):
    @abstractmethod
    def create(self, pokemon: Pokemon) -> Pokemon:
        pass

    @abstractmethod
    def get_by_id(self, pokemon_id: int) -> Pokemon | None:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Pokemon]:
        pass

    @abstractmethod
    def update(self, pokemon_id: int, trainer: Pokemon) -> Pokemon | None:
        pass

    @abstractmethod
    def delete(self, pokemon_id: int) -> bool:
        pass

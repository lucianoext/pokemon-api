from abc import ABC

from src.domain.repositories.base_repository import BaseRepository

from ..entities.pokemon import Pokemon


class PokemonRepository(BaseRepository[Pokemon], ABC):
    pass

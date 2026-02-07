from abc import ABC, abstractmethod

from src.domain.repositories.base_repository import BaseRepository

from ..entities.item import Item


class ItemRepository(BaseRepository[Item], ABC):
    @abstractmethod
    def get_by_type(self, item_type: str) -> list[Item]:
        pass

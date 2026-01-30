from abc import ABC, abstractmethod
from ..entities.item import Item

class ItemRepository(ABC):
    
    @abstractmethod
    def create(self, item: Item) -> Item:
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Item | None:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Item]:
        pass
    
    @abstractmethod
    def update(self, item_id: int, item: Item) -> Item | None:
        pass
    
    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_type(self, item_type: str) -> list[Item]:
        pass
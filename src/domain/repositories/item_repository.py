from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.item import Item

class ItemRepository(ABC):
    
    @abstractmethod
    def create(self, item: Item) -> Item:
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[Item]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Item]:
        pass
    
    @abstractmethod
    def update(self, item_id: int, item: Item) -> Optional[Item]:
        pass
    
    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_type(self, item_type: str) -> List[Item]:
        pass
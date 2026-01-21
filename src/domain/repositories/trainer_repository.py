from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.trainer import Trainer

class TrainerRepository(ABC):
    
    @abstractmethod
    def create(self, trainer: Trainer) -> Trainer:
        pass
    
    @abstractmethod
    def get_by_id(self, trainer_id: int) -> Optional[Trainer]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Trainer]:
        pass
    
    @abstractmethod
    def update(self, trainer_id: int, trainer: Trainer) -> Optional[Trainer]:
        pass
    
    @abstractmethod
    def delete(self, trainer_id: int) -> bool:
        pass
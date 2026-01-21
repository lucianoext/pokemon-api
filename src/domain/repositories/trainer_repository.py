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
        
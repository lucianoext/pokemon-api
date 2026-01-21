from typing import List, Optional
from src.domain.repositories.trainer_repository import TrainerRepository
from src.domain.entities.trainer import Trainer
from src.application.dtos.trainer_dto import (
    TrainerCreateDTO, 
    TrainerResponseDTO, 
    TrainerUpdateDTO
)

class TrainerService:
    def __init__(self, trainer_repository: TrainerRepository):
        self.trainer_repository = trainer_repository
    
    def create_trainer(self, trainer_dto: TrainerCreateDTO) -> TrainerResponseDTO:
        trainer = Trainer(
            id=None,
            name=trainer_dto.name,
            gender=trainer_dto.gender,
            region=trainer_dto.region
        )
        
        created_trainer = self.trainer_repository.create(trainer)
        return self._transform_to_response_dto(created_trainer)
    
    def get_trainer(self, trainer_id: int) -> Optional[TrainerResponseDTO]:
        trainer = self.trainer_repository.get_by_id(trainer_id)
        return self._transform_to_response_dto(trainer) if trainer else None
    
    def get_all_trainers(self, skip: int = 0, limit: int = 100) -> List[TrainerResponseDTO]:
        trainers = self.trainer_repository.get_all(skip, limit)
        return [self._transform_to_response_dto(trainer) for trainer in trainers]
    
    def update_trainer(self, trainer_id: int, trainer_dto: TrainerUpdateDTO) -> Optional[TrainerResponseDTO]:
        existing_trainer = self.trainer_repository.get_by_id(trainer_id)
        
        if not existing_trainer:
            return None
        
        if trainer_dto.name is not None:
            existing_trainer.name = trainer_dto.name
        if trainer_dto.gender is not None:
            existing_trainer.gender = trainer_dto.gender
        if trainer_dto.region is not None:
            existing_trainer.region = trainer_dto.region
        
        updated_trainer = self.trainer_repository.update(trainer_id, existing_trainer)
        return self._transform_to_response_dto(updated_trainer) if updated_trainer else None
    
    def delete_trainer(self, trainer_id: int) -> bool:
        return self.trainer_repository.delete(trainer_id)
    
    def _transform_to_response_dto(self, trainer: Trainer) -> TrainerResponseDTO:
        return TrainerResponseDTO(
            id=trainer.id,
            name=trainer.name,
            gender=trainer.gender.value,
            region=trainer.region.value,
            team_size=0,
            pokemon_team=[]
        )
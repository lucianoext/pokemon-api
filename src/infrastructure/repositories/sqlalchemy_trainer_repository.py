from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.repositories.trainer_repository import TrainerRepository
from src.domain.entities.trainer import Trainer, Gender, Region
from src.infrastructure.database.models import TrainerModel

class SqlAlchemyTrainerRepository(TrainerRepository):
    
    def __init__(self, db: Session):
        self.db = db                
    
    def create(self, trainer: Trainer) -> Trainer:
        db_trainer = TrainerModel(
            name=trainer.name,
            gender=trainer.gender.value,
            region=trainer.region.value
        )
        
        self.db.add(db_trainer)       
        self.db.commit()              
        self.db.refresh(db_trainer)   
        
        return self._model_to_entity(db_trainer)  # Mapear de vuelta
    
    def get_by_id(self, trainer_id: int) -> Optional[Trainer]:
        db_trainer = self.db.query(TrainerModel).filter(
            TrainerModel.id == trainer_id
        ).first()
        
        return self._model_to_entity(db_trainer) if db_trainer else None
    
    def _model_to_entity(self, model: TrainerModel) -> Trainer:
        return Trainer(
            id=model.id,
            name=model.name,
            gender=Gender(model.gender),
            region=Region(model.region)
        )
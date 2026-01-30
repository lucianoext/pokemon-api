from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.repositories.trainer_repository import TrainerRepository
from src.domain.entities.trainer import Trainer, Gender, Region
from src.persistence.database.models import TrainerModel

class SqlAlchemyTrainerRepository(TrainerRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, trainer: Trainer) -> Trainer:
        db_trainer = TrainerModel(
            name=trainer.name,
            gender=self._get_enum_value(trainer.gender),
            region=self._get_enum_value(trainer.region)
        )
        self.db.add(db_trainer)
        self.db.commit()
        self.db.refresh(db_trainer)
        
        return self._model_to_entity(db_trainer)
    
    def get_by_id(self, trainer_id: int) -> Optional[Trainer]:
        db_trainer = self.db.query(TrainerModel).filter(
            TrainerModel.id == trainer_id
        ).first()
        
        return self._model_to_entity(db_trainer) if db_trainer else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Trainer]:
        db_trainers = self.db.query(TrainerModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(trainer) for trainer in db_trainers]
    
    def update(self, trainer_id: int, trainer: Trainer) -> Optional[Trainer]:
        db_trainer = self.db.query(TrainerModel).filter(
            TrainerModel.id == trainer_id
        ).first()
        
        if not db_trainer:
            return None
        
        db_trainer.name = trainer.name
        db_trainer.gender = self._get_enum_value(trainer.gender)
        db_trainer.region = self._get_enum_value(trainer.region)
        
        self.db.commit()
        self.db.refresh(db_trainer)
        
        return self._model_to_entity(db_trainer)
    
    def delete(self, trainer_id: int) -> bool:
        db_trainer = self.db.query(TrainerModel).filter(
            TrainerModel.id == trainer_id
        ).first()
        
        if not db_trainer:
            return False
        
        self.db.delete(db_trainer)
        self.db.commit()
        return True
    
    def _model_to_entity(self, model: TrainerModel) -> Trainer:
        return Trainer(
            id=model.id,
            name=model.name,
            gender=Gender(model.gender),
            region=Region(model.region)
        )
    
    def _get_enum_value(self, field) -> str:
        if hasattr(field, 'value'):
            return field.value 
        else:
            return str(field)
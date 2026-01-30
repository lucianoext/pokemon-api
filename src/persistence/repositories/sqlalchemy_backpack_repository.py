from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.domain.repositories.backpack_repository import BackpackRepository
from src.domain.entities.backpack import Backpack
from src.persistence.database.models import BackpackModel

class SqlAlchemyBackpackRepository(BackpackRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_item(self, backpack: Backpack) -> Backpack:
        existing = self.db.query(BackpackModel).filter(
            and_(
                BackpackModel.trainer_id == backpack.trainer_id,
                BackpackModel.item_id == backpack.item_id
            )
        ).first()
        
        if existing:
            existing.quantity += backpack.quantity
            self.db.commit()
            self.db.refresh(existing)
            return self._model_to_entity(existing)
        else:
            db_backpack = BackpackModel(
                trainer_id=backpack.trainer_id,
                item_id=backpack.item_id,
                quantity=backpack.quantity
            )
            
            self.db.add(db_backpack)
            self.db.commit()
            self.db.refresh(db_backpack)
            
            return self._model_to_entity(db_backpack)
    
    def remove_item(self, trainer_id: int, item_id: int, quantity: int) -> bool:
        db_backpack = self.db.query(BackpackModel).filter(
            and_(
                BackpackModel.trainer_id == trainer_id,
                BackpackModel.item_id == item_id
            )
        ).first()
        
        if not db_backpack:
            return False
        
        if db_backpack.quantity <= quantity:
            self.db.delete(db_backpack)
        else:
            db_backpack.quantity -= quantity
        
        self.db.commit()
        return True
    
    def get_trainer_backpack(self, trainer_id: int) -> list[Backpack]:
        db_backpacks = self.db.query(BackpackModel).filter(
            BackpackModel.trainer_id == trainer_id
        ).all()
        
        return [self._model_to_entity(backpack) for backpack in db_backpacks]
    
    def get_item_quantity(self, trainer_id: int, item_id: int) -> int:
        db_backpack = self.db.query(BackpackModel).filter(
            and_(
                BackpackModel.trainer_id == trainer_id,
                BackpackModel.item_id == item_id
            )
        ).first()
        
        return db_backpack.quantity if db_backpack else 0
    
    def update_quantity(self, trainer_id: int, item_id: int, new_quantity: int) -> Backpack | None:
        db_backpack = self.db.query(BackpackModel).filter(
            and_(
                BackpackModel.trainer_id == trainer_id,
                BackpackModel.item_id == item_id
            )
        ).first()
        
        if not db_backpack:
            return None
        
        if new_quantity <= 0:
            self.db.delete(db_backpack)
            self.db.commit()
            return None
        else:
            db_backpack.quantity = new_quantity
            self.db.commit()
            self.db.refresh(db_backpack)
            return self._model_to_entity(db_backpack)
    
    def clear_backpack(self, trainer_id: int) -> bool:
        deleted_count = self.db.query(BackpackModel).filter(
            BackpackModel.trainer_id == trainer_id
        ).delete()
        
        self.db.commit()
        return deleted_count > 0
    
    def _model_to_entity(self, model: BackpackModel) -> Backpack:
        return Backpack(
            id=model.id,
            trainer_id=model.trainer_id,
            item_id=model.item_id,
            quantity=model.quantity
        )
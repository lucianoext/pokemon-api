from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.domain.entities.backpack import Backpack
from src.domain.repositories.backpack_repository import BackpackRepository
from src.persistence.database.models import BackpackModel
from src.persistence.repositories.base_sqlmodel_repository import BaseSqlModelRepository


class SqlModelBackpackRepository(
    BaseSqlModelRepository[Backpack, BackpackModel], BackpackRepository
):
    """SQLModel-based Backpack repository with generics."""

    def __init__(self, db: Session):
        super().__init__(
            db=db,
            model_class=BackpackModel,
            entity_to_model_mapper=self._entity_to_model,
            model_to_entity_mapper=self._model_to_entity,
        )

    def _entity_to_model(self, backpack: Backpack) -> BackpackModel:
        """Convert Backpack entity to SQLModel."""
        return BackpackModel(
            id=backpack.id,
            trainer_id=backpack.trainer_id,
            item_id=backpack.item_id,
            quantity=backpack.quantity,
        )

    def _model_to_entity(self, model: BackpackModel) -> Backpack:
        """Convert SQLModel to Backpack entity."""
        return Backpack(
            id=model.id,
            trainer_id=model.trainer_id,
            item_id=model.item_id,
            quantity=model.quantity,
        )

    # Domain-specific methods
    def add_item(self, backpack: Backpack) -> Backpack:
        """Add item to backpack - custom logic with quantity merging."""
        existing = (
            self.db.query(BackpackModel)
            .filter(
                and_(
                    BackpackModel.trainer_id == backpack.trainer_id,
                    BackpackModel.item_id == backpack.item_id,
                )
            )
            .first()
        )

        if existing:
            existing.quantity += backpack.quantity
            self.db.commit()
            self.db.refresh(existing)
            return self._model_to_entity(existing)
        else:
            return self.create(backpack)  # Use generic create

    def remove_item(self, trainer_id: int, item_id: int, quantity: int) -> bool:
        """Remove item from backpack - custom logic."""
        db_backpack = (
            self.db.query(BackpackModel)
            .filter(
                and_(
                    BackpackModel.trainer_id == trainer_id,
                    BackpackModel.item_id == item_id,
                )
            )
            .first()
        )

        if not db_backpack:
            return False

        if db_backpack.quantity <= quantity:
            self.db.delete(db_backpack)
        else:
            db_backpack.quantity -= quantity

        self.db.commit()
        return True

    def get_trainer_backpack(self, trainer_id: int) -> list[Backpack]:
        """Get trainer's backpack - custom query."""
        db_backpacks = (
            self.db.query(BackpackModel)
            .filter(BackpackModel.trainer_id == trainer_id)
            .all()
        )
        return [self._model_to_entity(backpack) for backpack in db_backpacks]

    def get_item_quantity(self, trainer_id: int, item_id: int) -> int:
        """Get item quantity - custom query."""
        db_backpack = (
            self.db.query(BackpackModel)
            .filter(
                and_(
                    BackpackModel.trainer_id == trainer_id,
                    BackpackModel.item_id == item_id,
                )
            )
            .first()
        )
        return db_backpack.quantity if db_backpack else 0

    def update_quantity(
        self, trainer_id: int, item_id: int, new_quantity: int
    ) -> Backpack | None:
        """Update item quantity - custom logic."""
        db_backpack = (
            self.db.query(BackpackModel)
            .filter(
                and_(
                    BackpackModel.trainer_id == trainer_id,
                    BackpackModel.item_id == item_id,
                )
            )
            .first()
        )

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
        """Clear backpack - custom logic."""
        deleted_count = (
            self.db.query(BackpackModel)
            .filter(BackpackModel.trainer_id == trainer_id)
            .delete()
        )
        self.db.commit()
        return bool(deleted_count > 0)

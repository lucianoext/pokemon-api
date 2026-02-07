# src/persistence/repositories/sqlmodel_trainer_repository.py
from typing import Any

from sqlalchemy.orm import Session

from src.domain.entities.trainer import Gender, Region, Trainer
from src.domain.repositories.trainer_repository import TrainerRepository
from src.persistence.database.models import TrainerModel
from src.persistence.repositories.base_sqlmodel_repository import BaseSqlModelRepository


class SqlModelTrainerRepository(
    BaseSqlModelRepository[Trainer, TrainerModel], TrainerRepository
):
    """SQLModel-based Trainer repository with generics."""

    def __init__(self, db: Session):
        super().__init__(
            db=db,
            model_class=TrainerModel,
            entity_to_model_mapper=self._entity_to_model,
            model_to_entity_mapper=self._model_to_entity,
        )

    def _entity_to_model(self, trainer: Trainer) -> TrainerModel:
        """Convert Trainer entity to SQLModel."""
        return TrainerModel(
            id=trainer.id,
            name=trainer.name,
            gender=self._get_enum_value(trainer.gender),
            region=self._get_enum_value(trainer.region),
        )

    def _model_to_entity(self, model: TrainerModel) -> Trainer:
        """Convert SQLModel to Trainer entity."""
        return Trainer(
            id=model.id,
            name=model.name,
            gender=Gender(model.gender),
            region=Region(model.region),
        )

    def _get_enum_value(self, field: Any) -> str | None:
        """Get string value from enum."""
        if field is None:
            return None
        return field.value if hasattr(field, "value") else str(field)

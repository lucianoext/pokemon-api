from typing import Any

from sqlalchemy.orm import Session, selectinload

from src.domain.entities.trainer import Gender, Region, Trainer
from src.domain.repositories.trainer_repository import TrainerRepository
from src.persistence.database.models import TeamModel, TrainerModel
from src.persistence.repositories.base_sqlmodel_repository import BaseSqlModelRepository


class SqlModelTrainerRepository(
    BaseSqlModelRepository[Trainer, TrainerModel], TrainerRepository
):
    def __init__(self, db: Session):
        super().__init__(
            db=db,
            model_class=TrainerModel,
            entity_to_model_mapper=self._entity_to_model,
            model_to_entity_mapper=self._model_to_entity,
        )

    def get_by_id(self, entity_id: int) -> Trainer | None:
        model = (
            self.db.query(self.model_class)
            .options(
                selectinload(TrainerModel.team_members).joinedload(TeamModel.pokemon)
            )
            .filter(self.model_class.id == entity_id)
            .first()
        )
        return self._model_to_entity(model) if model else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Trainer]:
        models = (
            self.db.query(self.model_class)
            .options(
                selectinload(TrainerModel.team_members).joinedload(TeamModel.pokemon)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._model_to_entity(model) for model in models]

    def _entity_to_model(self, trainer: Trainer) -> TrainerModel:
        return TrainerModel(
            id=trainer.id,
            name=trainer.name,
            gender=self._get_enum_value(trainer.gender),
            region=self._get_enum_value(trainer.region),
        )

    def _model_to_entity(self, model: TrainerModel) -> Trainer:
        return Trainer(
            id=model.id,
            name=model.name,
            gender=Gender(model.gender),
            region=Region(model.region),
        )

    def _get_enum_value(self, field: Any) -> str | None:
        if field is None:
            return None
        return field.value if hasattr(field, "value") else str(field)

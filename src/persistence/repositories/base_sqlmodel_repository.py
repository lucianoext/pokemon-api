from collections.abc import Callable
from typing import TypeVar

from sqlalchemy.orm import Session
from sqlmodel import SQLModel, select

from src.domain.protocols.entity_protocol import EntityProtocol
from src.domain.repositories.base_repository import BaseRepository

EntityType = TypeVar("EntityType", bound=EntityProtocol)
ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseSqlModelRepository[EntityType: EntityProtocol, ModelType: SQLModel](
    BaseRepository[EntityType]
):
    """Generic SQLModel repository implementation with full CRUD logic."""

    def __init__(
        self,
        db: Session,
        model_class: type[ModelType],
        entity_to_model_mapper: Callable[[EntityType], ModelType],
        model_to_entity_mapper: Callable[[ModelType], EntityType],
    ):
        """Initialize with database session and mapping functions."""
        self.db = db
        self.model_class = model_class
        self._entity_to_model = entity_to_model_mapper
        self._model_to_entity = model_to_entity_mapper

    def create(self, entity: EntityType) -> EntityType:
        """Create a new entity in the database."""
        db_model = self._entity_to_model(entity)
        self.db.add(db_model)
        self.db.commit()
        self.db.refresh(db_model)
        return self._model_to_entity(db_model)

    def get_by_id(self, entity_id: int) -> EntityType | None:
        """Get entity by ID from database."""
        db_model = self.db.get(self.model_class, entity_id)
        return self._model_to_entity(db_model) if db_model else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[EntityType]:
        """Get all entities with pagination."""
        statement = select(self.model_class).offset(skip).limit(limit)
        db_models = self.db.exec(statement).all()
        return [self._model_to_entity(model) for model in db_models]

    def update(self, entity_id: int, entity: EntityType) -> EntityType | None:
        """Update an existing entity."""
        db_model = self.db.get(self.model_class, entity_id)
        if not db_model:
            return None

        updated_model = self._entity_to_model(entity)
        for field, value in updated_model.model_dump(exclude_unset=True).items():
            if hasattr(db_model, field) and field != "id":
                setattr(db_model, field, value)

        self.db.add(db_model)
        self.db.commit()
        self.db.refresh(db_model)
        return self._model_to_entity(db_model)

    def delete(self, entity_id: int) -> bool:
        """Delete an entity by ID."""
        db_model = self.db.get(self.model_class, entity_id)
        if not db_model:
            return False

        self.db.delete(db_model)
        self.db.commit()
        return True

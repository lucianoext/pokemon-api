from typing import Any

from sqlalchemy.orm import Session
from sqlmodel import select

from src.domain.entities.item import Item, ItemType
from src.domain.repositories.item_repository import ItemRepository
from src.persistence.database.models import ItemModel
from src.persistence.repositories.base_sqlmodel_repository import BaseSqlModelRepository


class SqlModelItemRepository(BaseSqlModelRepository[Item, ItemModel], ItemRepository):
    """SQLModel-based Item repository with generics."""

    def __init__(self, db: Session):
        super().__init__(
            db=db,
            model_class=ItemModel,
            entity_to_model_mapper=self._entity_to_model,
            model_to_entity_mapper=self._model_to_entity,
        )

    def _entity_to_model(self, item: Item) -> ItemModel:
        """Convert Item entity to SQLModel."""
        return ItemModel(
            id=item.id,
            name=item.name,
            type=self._get_enum_value(item.type),
            description=item.description,
            price=item.price,
        )

    def _model_to_entity(self, model: ItemModel) -> Item:
        """Convert SQLModel to Item entity."""
        return Item(
            id=model.id,
            name=model.name,
            type=ItemType(model.type),
            description=model.description or "",
            price=model.price,
        )

    def _get_enum_value(self, field: Any) -> str | None:
        """Get string value from enum."""
        if field is None:
            return None
        return field.value if hasattr(field, "value") else str(field)

    # Domain-specific method (only one not covered by generics)
    def get_by_type(self, item_type: str) -> list[Item]:
        """Get items by type - domain-specific method."""
        statement = select(ItemModel).where(ItemModel.type == item_type)
        db_models = self.db.exec(statement).all()
        return [self._model_to_entity(model) for model in db_models]

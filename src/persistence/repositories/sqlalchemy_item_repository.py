from typing import Any

from sqlalchemy.orm import Session

from src.domain.entities.item import Item, ItemType
from src.domain.repositories.item_repository import ItemRepository
from src.persistence.database.models import ItemModel


class SqlAlchemyItemRepository(ItemRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, item: Item) -> Item:
        db_item = ItemModel(
            name=item.name,
            type=self._get_enum_value(item.type),
            description=item.description,
            price=item.price,
        )

        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)

        return self._model_to_entity(db_item)

    def get_by_id(self, item_id: int) -> Item | None:
        db_item = self.db.query(ItemModel).filter(ItemModel.id == item_id).first()

        return self._model_to_entity(db_item) if db_item else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Item]:
        db_items = self.db.query(ItemModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(item) for item in db_items]

    def update(self, item_id: int, item: Item) -> Item | None:
        db_item = self.db.query(ItemModel).filter(ItemModel.id == item_id).first()

        if not db_item:
            return None

        db_item.name = item.name
        db_item.type = self._get_enum_value(item.type)
        db_item.description = item.description
        db_item.price = item.price

        self.db.commit()
        self.db.refresh(db_item)

        return self._model_to_entity(db_item)

    def delete(self, item_id: int) -> bool:
        db_item = self.db.query(ItemModel).filter(ItemModel.id == item_id).first()

        if not db_item:
            return False

        self.db.delete(db_item)
        self.db.commit()
        return True

    def get_by_type(self, item_type: str) -> list[Item]:
        db_items = self.db.query(ItemModel).filter(ItemModel.type == item_type).all()
        return [self._model_to_entity(item) for item in db_items]

    def _model_to_entity(self, model: ItemModel) -> Item:
        return Item(
            id=model.id,
            name=model.name,
            type=ItemType(model.type),
            description=model.description or "",
            price=model.price,
        )

    def _get_enum_value(self, field: Any) -> str | None:
        if field is None:
            return None
        if hasattr(field, "value"):
            return str(field.value)
        return str(field)

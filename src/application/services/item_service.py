from src.application.dtos.item_dto import ItemCreateDTO, ItemResponseDTO, ItemUpdateDTO
from src.application.services.base_service import BaseService
from src.domain.entities.item import Item
from src.domain.exceptions import BusinessRuleException
from src.domain.repositories.item_repository import ItemRepository


class ItemService(BaseService[Item, ItemCreateDTO, ItemUpdateDTO, ItemResponseDTO]):
    def __init__(self, item_repository: ItemRepository):
        super().__init__(item_repository)
        self.item_repository = item_repository

    def create_item(self, dto: ItemCreateDTO) -> ItemResponseDTO:
        return self.create(dto)

    def get_item(self, item_id: int) -> ItemResponseDTO | None:
        return self.get_by_id(item_id)

    def get_all_items(self, skip: int = 0, limit: int = 100) -> list[ItemResponseDTO]:
        return self.get_all(skip, limit)

    def update_item(self, item_id: int, dto: ItemUpdateDTO) -> ItemResponseDTO | None:
        return self.update(item_id, dto)

    def delete_item(self, item_id: int) -> bool:
        return self.delete(item_id)

    def get_items_by_type(self, item_type: str) -> list[ItemResponseDTO]:
        items = self.item_repository.get_by_type(item_type)
        return [self._transform_to_response_dto(item) for item in items]

    def _validate_business_rules_for_creation(self, dto: ItemCreateDTO) -> None:
        if dto.price < 0:
            raise BusinessRuleException("Item price cannot be negative")

        if len(dto.name.strip()) == 0:
            raise BusinessRuleException("Item name cannot be empty")

    def _validate_business_rules_for_update(self, item: Item) -> None:
        if item.price < 0:
            raise BusinessRuleException("Item price cannot be negative")

        if len(item.name.strip()) == 0:
            raise BusinessRuleException("Item name cannot be empty")

    def _dto_to_entity(self, dto: ItemCreateDTO) -> Item:
        return Item(
            id=None,
            name=dto.name,
            type=dto.type,
            description=dto.description,
            price=dto.price,
        )

    def _transform_to_response_dto(self, item: Item) -> ItemResponseDTO:
        return ItemResponseDTO(
            id=item.id,
            name=item.name,
            type=item.type.value,
            description=item.description,
            price=item.price,
        )

    def _apply_update_dto(self, existing_item: Item, dto: ItemUpdateDTO) -> Item:
        non_none_fields = self._get_dto_non_none_fields(dto)

        return Item(
            id=existing_item.id,
            name=non_none_fields.get("name", existing_item.name),
            type=non_none_fields.get("type", existing_item.type),
            description=non_none_fields.get("description", existing_item.description),
            price=non_none_fields.get("price", existing_item.price),
        )

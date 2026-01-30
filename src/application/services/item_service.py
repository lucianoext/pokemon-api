from src.domain.repositories.item_repository import ItemRepository
from src.domain.entities.item import Item
from src.application.dtos.item_dto import (
    ItemCreateDTO,
    ItemUpdateDTO,
    ItemResponseDTO
)
from src.domain.exceptions import BusinessRuleException

class ItemService:
    
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
    
    def create_item(self, dto: ItemCreateDTO) -> ItemResponseDTO:
        self._validate_business_rules_for_creation(dto)
        item = self._dto_to_entity(dto)
        created_item = self.item_repository.create(item)
        return self._transform_to_response_dto(created_item)
    
    def get_item(self, item_id: int) -> ItemResponseDTO | None:
        item = self.item_repository.get_by_id(item_id)
        if not item:
            return None
        return self._transform_to_response_dto(item)
    
    def get_all_items(self, skip: int = 0, limit: int = 100) -> list[ItemResponseDTO]:
        items = self.item_repository.get_all(skip, limit)
        return [self._transform_to_response_dto(item) for item in items]
    
    def update_item(self, item_id: int, dto: ItemUpdateDTO) -> ItemResponseDTO | None:
        existing_item = self.item_repository.get_by_id(item_id)
        if not existing_item:
            return None
        
        updated_item = Item(
            id=existing_item.id,
            name=dto.name if dto.name is not None else existing_item.name,
            type=dto.type if dto.type is not None else existing_item.type,
            description=dto.description if dto.description is not None else existing_item.description,
            price=dto.price if dto.price is not None else existing_item.price
        )
        
        self._validate_business_rules_for_update(updated_item)
        
        saved_item = self.item_repository.update(item_id, updated_item)
        return self._transform_to_response_dto(saved_item) if saved_item else None
    
    def delete_item(self, item_id: int) -> bool:
        return self.item_repository.delete(item_id)
    
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
            price=dto.price
        )
    
    def _transform_to_response_dto(self, item: Item) -> ItemResponseDTO:
        return ItemResponseDTO(
            id=item.id,
            name=item.name,
            type=item.type.value,
            description=item.description,
            price=item.price
        )
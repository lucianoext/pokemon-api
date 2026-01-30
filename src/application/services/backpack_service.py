from src.domain.repositories.backpack_repository import BackpackRepository
from src.domain.repositories.trainer_repository import TrainerRepository
from src.domain.repositories.item_repository import ItemRepository
from src.domain.entities.backpack import Backpack
from src.application.dtos.backpack_dto import (
    BackpackAddItemDTO,
    BackpackRemoveItemDTO,
    BackpackUpdateQuantityDTO,
    BackpackItemResponseDTO,
    BackpackResponseDTO
)
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException

class BackpackService:
    
    def __init__(
        self,
        backpack_repository: BackpackRepository,
        trainer_repository: TrainerRepository,
        item_repository: ItemRepository
    ):
        self.backpack_repository = backpack_repository
        self.trainer_repository = trainer_repository
        self.item_repository = item_repository
    
    def add_item_to_backpack(self, dto: BackpackAddItemDTO) -> BackpackResponseDTO:
        
        trainer = self.trainer_repository.get_by_id(dto.trainer_id)
        if not trainer:
            raise EntityNotFoundException("Trainer", dto.trainer_id)
        
        item = self.item_repository.get_by_id(dto.item_id)
        if not item:
            raise EntityNotFoundException("Item", dto.item_id)
        
        self._validate_add_item_rules(dto)
        
        backpack_entry = Backpack(
            id=None,
            trainer_id=dto.trainer_id,
            item_id=dto.item_id,
            quantity=dto.quantity
        )
        
        self.backpack_repository.add_item(backpack_entry)
        
        return self.get_trainer_backpack(dto.trainer_id)
    
    def remove_item_from_backpack(
        self,
        trainer_id: int,
        item_id: int,
        dto: BackpackRemoveItemDTO
    ) -> BackpackResponseDTO:
        
        current_quantity = self.backpack_repository.get_item_quantity(trainer_id, item_id)
        if current_quantity == 0:
            raise BusinessRuleException(f"Trainer {trainer_id} doesn't have item {item_id}")
        
        if dto.quantity > current_quantity:
            raise BusinessRuleException(
                f"Cannot remove {dto.quantity} items. Only {current_quantity} available"
            )
        
        success = self.backpack_repository.remove_item(trainer_id, item_id, dto.quantity)
        
        if not success:
            raise BusinessRuleException("Failed to remove item from backpack")
        
        return self.get_trainer_backpack(trainer_id)
    
    def update_item_quantity(
        self,
        trainer_id: int,
        item_id: int,
        dto: BackpackUpdateQuantityDTO
    ) -> BackpackResponseDTO:
        
        current_quantity = self.backpack_repository.get_item_quantity(trainer_id, item_id)
        if current_quantity == 0:
            raise BusinessRuleException(f"Trainer {trainer_id} doesn't have item {item_id}")
        
        if dto.new_quantity < 0:
            raise BusinessRuleException("Quantity cannot be negative")
        
        if dto.new_quantity > 999:
            raise BusinessRuleException("Maximum 999 items of each type allowed")
        
        self.backpack_repository.update_quantity(trainer_id, item_id, dto.new_quantity)
        
        return self.get_trainer_backpack(trainer_id)
    
    def get_trainer_backpack(self, trainer_id: int) -> BackpackResponseDTO:
        
        trainer = self.trainer_repository.get_by_id(trainer_id)
        if not trainer:
            raise EntityNotFoundException("Trainer", trainer_id)
        
        backpack_items = self.backpack_repository.get_trainer_backpack(trainer_id)
        
        item_dtos = []
        for backpack_item in backpack_items:
            item = self.item_repository.get_by_id(backpack_item.item_id)
            if item:
                item_dto = BackpackItemResponseDTO(
                    id=backpack_item.id,
                    trainer_id=backpack_item.trainer_id,
                    item_id=backpack_item.item_id,
                    item_name=item.name,
                    item_type=item.type.value,
                    item_description=item.description,
                    item_price=item.price,
                    quantity=backpack_item.quantity
                )
                item_dtos.append(item_dto)
        
        return BackpackResponseDTO(
            trainer_id=trainer_id,
            trainer_name=trainer.name,
            total_items=sum(item.quantity for item in item_dtos),
            items=item_dtos
        )
    
    def clear_backpack(self, trainer_id: int) -> BackpackResponseDTO:
        
        trainer = self.trainer_repository.get_by_id(trainer_id)
        if not trainer:
            raise EntityNotFoundException("Trainer", trainer_id)
        
        self.backpack_repository.clear_backpack(trainer_id)
        
        return self.get_trainer_backpack(trainer_id)
    
    def _validate_add_item_rules(self, dto: BackpackAddItemDTO) -> None:
        
        if dto.quantity <= 0:
            raise BusinessRuleException("Quantity must be positive")
        
        current_quantity = self.backpack_repository.get_item_quantity(dto.trainer_id, dto.item_id)
        total_quantity = current_quantity + dto.quantity
        
        if total_quantity > 999:
            raise BusinessRuleException(
                f"Maximum 999 items allowed. Current: {current_quantity}, "
                f"trying to add: {dto.quantity}, total would be: {total_quantity}"
            )
from unittest.mock import Mock

import pytest

from src.application.services.backpack_service import BackpackService
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException
from tests.factories.backpack_factories import (
    BackpackAddItemDTOFactory,
    BackpackFactory,
    BackpackRemoveItemDTOFactory,
    BackpackUpdateQuantityDTOFactory,
)
from tests.factories.item_factories import ItemFactory
from tests.factories.trainer_factories import TrainerFactory


class TestBackpackService:
    @pytest.fixture
    def backpack_service(
        self,
        mock_backpack_repository: Mock,
        mock_trainer_repository: Mock,
        mock_item_repository: Mock,
    ) -> BackpackService:
        return BackpackService(
            backpack_repository=mock_backpack_repository,
            trainer_repository=mock_trainer_repository,
            item_repository=mock_item_repository,
        )

    def test_add_item_to_backpack_success(
        self,
        backpack_service: BackpackService,
        mock_backpack_repository: Mock,
        mock_trainer_repository: Mock,
        mock_item_repository: Mock,
    ) -> None:
        add_dto = BackpackAddItemDTOFactory.add_potion_to_ash()
        trainer = TrainerFactory.ash_ketchum()
        item = ItemFactory.potion()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_item_repository.get_by_id.return_value = item
        mock_backpack_repository.get_item_quantity.return_value = 0
        mock_backpack_repository.get_trainer_backpack.return_value = []

        mock_backpack_repository.add_item.return_value = None

        result = backpack_service.add_item_to_backpack(add_dto)

        assert result.trainer_id == trainer.id
        assert result.trainer_name == trainer.name
        assert result.total_items == 0
        mock_trainer_repository.get_by_id.assert_called_with(1)
        mock_item_repository.get_by_id.assert_called_once_with(1)
        mock_backpack_repository.add_item.assert_called_once()

    def test_add_item_trainer_not_found(
        self, backpack_service: BackpackService, mock_trainer_repository: Mock
    ) -> None:
        add_dto = BackpackAddItemDTOFactory.add_potion_to_ash()
        mock_trainer_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Trainer.*1"):
            backpack_service.add_item_to_backpack(add_dto)

    def test_add_item_item_not_found(
        self,
        backpack_service: BackpackService,
        mock_trainer_repository: Mock,
        mock_item_repository: Mock,
    ) -> None:
        add_dto = BackpackAddItemDTOFactory.add_potion_to_ash()
        trainer = TrainerFactory.ash_ketchum()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_item_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Item.*1"):
            backpack_service.add_item_to_backpack(add_dto)

    def test_add_item_negative_quantity(
        self, backpack_service: BackpackService, mock_backpack_repository: Mock
    ) -> None:
        add_dto = BackpackAddItemDTOFactory.add_negative_quantity()
        mock_backpack_repository.get_item_quantity.return_value = 0

        with pytest.raises(BusinessRuleException, match="Quantity must be positive"):
            backpack_service.add_item_to_backpack(add_dto)

    def test_add_item_zero_quantity(
        self, backpack_service: BackpackService, mock_backpack_repository: Mock
    ) -> None:
        add_dto = BackpackAddItemDTOFactory.add_zero_quantity()
        mock_backpack_repository.get_item_quantity.return_value = 0

        with pytest.raises(BusinessRuleException, match="Quantity must be positive"):
            backpack_service.add_item_to_backpack(add_dto)

    def test_add_item_exceeds_maximum(
        self,
        backpack_service: BackpackService,
        mock_trainer_repository: Mock,
        mock_item_repository: Mock,
        mock_backpack_repository: Mock,
    ) -> None:
        add_dto = BackpackAddItemDTOFactory.add_large_quantity()
        trainer = TrainerFactory.ash_ketchum()
        item = ItemFactory.potion()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_item_repository.get_by_id.return_value = item
        mock_backpack_repository.get_item_quantity.return_value = 980

        with pytest.raises(BusinessRuleException, match="Maximum 999 items allowed"):
            backpack_service.add_item_to_backpack(add_dto)

    def test_remove_item_from_backpack_success(
        self,
        backpack_service: BackpackService,
        mock_backpack_repository: Mock,
        mock_trainer_repository: Mock,
    ) -> None:
        remove_dto = BackpackRemoveItemDTOFactory.remove_one()
        trainer = TrainerFactory.ash_ketchum()

        mock_backpack_repository.get_item_quantity.return_value = 5
        mock_backpack_repository.remove_item.return_value = True
        mock_trainer_repository.get_by_id.return_value = trainer
        mock_backpack_repository.get_trainer_backpack.return_value = []

        result = backpack_service.remove_item_from_backpack(1, 1, remove_dto)

        assert result.trainer_id == 1
        mock_backpack_repository.remove_item.assert_called_once_with(1, 1, 1)

    def test_remove_item_not_in_backpack(
        self, backpack_service: BackpackService, mock_backpack_repository: Mock
    ) -> None:
        remove_dto = BackpackRemoveItemDTOFactory.remove_one()
        mock_backpack_repository.get_item_quantity.return_value = 0

        with pytest.raises(BusinessRuleException, match="doesn't have item"):
            backpack_service.remove_item_from_backpack(1, 999, remove_dto)

    def test_remove_item_insufficient_quantity(
        self, backpack_service: BackpackService, mock_backpack_repository: Mock
    ) -> None:
        remove_dto = BackpackRemoveItemDTOFactory.remove_more_than_available()
        mock_backpack_repository.get_item_quantity.return_value = 5

        with pytest.raises(BusinessRuleException, match="Cannot remove.*Only.*available"):
            backpack_service.remove_item_from_backpack(1, 1, remove_dto)

    def test_remove_item_operation_failed(
        self, backpack_service: BackpackService, mock_backpack_repository: Mock
    ) -> None:
        remove_dto = BackpackRemoveItemDTOFactory.remove_one()
        mock_backpack_repository.get_item_quantity.return_value = 5
        mock_backpack_repository.remove_item.return_value = False

        with pytest.raises(BusinessRuleException, match="Failed to remove item from backpack"):
            backpack_service.remove_item_from_backpack(1, 1, remove_dto)

    def test_update_item_quantity_success(
        self,
        backpack_service: BackpackService,
        mock_backpack_repository: Mock,
        mock_trainer_repository: Mock,
    ) -> None:
        update_dto = BackpackUpdateQuantityDTOFactory.update_to_ten()
        trainer = TrainerFactory.ash_ketchum()

        mock_backpack_repository.get_item_quantity.return_value = 5
        mock_backpack_repository.update_quantity.return_value = None
        mock_trainer_repository.get_by_id.return_value = trainer
        mock_backpack_repository.get_trainer_backpack.return_value = []

        result = backpack_service.update_item_quantity(1, 1, update_dto)

        assert result.trainer_id == 1
        mock_backpack_repository.update_quantity.assert_called_once_with(1, 1, 10)

    def test_update_item_quantity_negative_fails(
        self, backpack_service: BackpackService, mock_backpack_repository: Mock
    ) -> None:
        update_dto = BackpackUpdateQuantityDTOFactory.update_to_negative()
        mock_backpack_repository.get_item_quantity.return_value = 5

        with pytest.raises(BusinessRuleException, match="Quantity cannot be negative"):
            backpack_service.update_item_quantity(1, 1, update_dto)

    def test_update_item_quantity_exceeds_maximum(
        self,
        backpack_service: BackpackService,
        mock_backpack_repository: Mock,
        mock_trainer_repository: Mock,
    ) -> None:
        update_dto = BackpackUpdateQuantityDTOFactory.build(new_quantity=1000)
        trainer = TrainerFactory.ash_ketchum()

        mock_backpack_repository.get_item_quantity.return_value = 5
        mock_trainer_repository.get_by_id.return_value = trainer
        mock_backpack_repository.get_trainer_backpack.return_value = []

        with pytest.raises(BusinessRuleException, match="Maximum 999 items"):
            backpack_service.update_item_quantity(1, 1, update_dto)

    def test_update_item_quantity_not_in_backpack(
        self, backpack_service: BackpackService, mock_backpack_repository: Mock
    ) -> None:
        update_dto = BackpackUpdateQuantityDTOFactory.update_to_ten()
        mock_backpack_repository.get_item_quantity.return_value = 0

        with pytest.raises(BusinessRuleException, match="doesn't have item"):
            backpack_service.update_item_quantity(1, 999, update_dto)

    def test_get_trainer_backpack_success(
        self,
        backpack_service: BackpackService,
        mock_trainer_repository: Mock,
        mock_backpack_repository: Mock,
        mock_item_repository: Mock,
    ) -> None:
        trainer = TrainerFactory.ash_ketchum()
        backpack_items = [BackpackFactory.ash_potion_entry()]
        item = ItemFactory.potion()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_backpack_repository.get_trainer_backpack.return_value = backpack_items
        mock_item_repository.get_by_id.return_value = item

        result = backpack_service.get_trainer_backpack(1)

        assert result.trainer_id == 1
        assert result.trainer_name == "Ash Ketchum"
        assert result.total_items == 5
        assert len(result.items) == 1
        assert result.items[0].item_name == "Potion"
        assert result.items[0].quantity == 5

    def test_get_trainer_backpack_trainer_not_found(
        self, backpack_service: BackpackService, mock_trainer_repository: Mock
    ) -> None:
        mock_trainer_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Trainer.*999"):
            backpack_service.get_trainer_backpack(999)

    def test_get_trainer_backpack_empty(
        self,
        backpack_service: BackpackService,
        mock_trainer_repository: Mock,
        mock_backpack_repository: Mock,
    ) -> None:
        trainer = TrainerFactory.ash_ketchum()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_backpack_repository.get_trainer_backpack.return_value = []

        result = backpack_service.get_trainer_backpack(1)

        assert result.trainer_id == 1
        assert result.total_items == 0
        assert len(result.items) == 0

    def test_clear_backpack_success(
        self,
        backpack_service: BackpackService,
        mock_trainer_repository: Mock,
        mock_backpack_repository: Mock,
    ) -> None:
        trainer = TrainerFactory.ash_ketchum()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_backpack_repository.clear_backpack.return_value = None
        mock_backpack_repository.get_trainer_backpack.return_value = []

        result = backpack_service.clear_backpack(1)

        assert result.trainer_id == 1
        assert result.total_items == 0
        mock_backpack_repository.clear_backpack.assert_called_once_with(1)

    def test_clear_backpack_trainer_not_found(
        self, backpack_service: BackpackService, mock_trainer_repository: Mock
    ) -> None:
        mock_trainer_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Trainer.*999"):
            backpack_service.clear_backpack(999)

    def test_backpack_entity_negative_quantity_validation(self) -> None:
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            BackpackFactory.negative_quantity_entry()

    def test_backpack_entity_zero_quantity_allowed(self) -> None:
        backpack_item = BackpackFactory.zero_quantity_entry()
        assert backpack_item.quantity == 0

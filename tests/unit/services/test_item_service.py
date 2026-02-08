from unittest.mock import Mock

import pytest

from src.application.services.item_service import ItemService
from src.domain.enums.item_enums import ItemType  # ← AGREGAR ESTA LÍNEA
from src.domain.exceptions import BusinessRuleException
from tests.factories.item_factories import (
    ItemCreateDTOFactory,
    ItemFactory,
    ItemUpdateDTOFactory,
)

class TestItemService:
    @pytest.fixture
    def item_service(self, mock_item_repository: Mock) -> ItemService:
        return ItemService(item_repository=mock_item_repository)

    def test_create_item_success(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        create_dto = ItemCreateDTOFactory.super_potion()
        item = ItemFactory.potion()
        mock_item_repository.create.return_value = item

        result = item_service.create_item(create_dto)

        assert result.name == item.name
        assert result.type == item.type.value
        assert result.price == item.price
        mock_item_repository.create.assert_called_once()

    def test_create_item_multiple_types(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        create_dto = ItemCreateDTOFactory.pokeball()
        item = ItemFactory.master_ball()
        mock_item_repository.create.return_value = item

        result = item_service.create_item(create_dto)

        assert result is not None
        assert result.name == item.name
        mock_item_repository.create.assert_called_once()

    def test_create_item_free_price_success(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        create_dto = ItemCreateDTOFactory.free_item()
        item = ItemFactory.free_berry()
        mock_item_repository.create.return_value = item

        result = item_service.create_item(create_dto)

        assert result.price == 0
        mock_item_repository.create.assert_called_once()

    def test_create_item_negative_price_fails(
        self, item_service: ItemService
    ) -> None:
        create_dto = ItemCreateDTOFactory.negative_price()

        with pytest.raises(BusinessRuleException, match="Item price cannot be negative"):
            item_service.create_item(create_dto)

    def test_create_item_empty_name_fails(
        self, item_service: ItemService
    ) -> None:
        create_dto = ItemCreateDTOFactory.empty_name()

        with pytest.raises(BusinessRuleException, match="Item name cannot be empty"):
            item_service.create_item(create_dto)

    def test_get_item_found(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        item = ItemFactory.potion()
        mock_item_repository.get_by_id.return_value = item

        result = item_service.get_item(1)

        assert result is not None
        assert result.id == item.id
        assert result.name == item.name
        assert result.type == item.type.value
        mock_item_repository.get_by_id.assert_called_once_with(1)

    def test_get_item_not_found(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        mock_item_repository.get_by_id.return_value = None

        result = item_service.get_item(999)

        assert result is None
        mock_item_repository.get_by_id.assert_called_once_with(999)

    def test_get_all_items_success(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        item_list = ItemFactory.batch(size=4)
        mock_item_repository.get_all.return_value = item_list

        result = item_service.get_all_items(skip=0, limit=10)

        assert len(result) == 4
        for i, item_dto in enumerate(result):
            assert item_dto.name == item_list[i].name
            assert item_dto.type == item_list[i].type.value
        mock_item_repository.get_all.assert_called_once_with(0, 10)

    def test_get_all_items_empty_list(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        mock_item_repository.get_all.return_value = []

        result = item_service.get_all_items()

        assert len(result) == 0
        mock_item_repository.get_all.assert_called_once_with(0, 100)

    def test_get_all_items_with_pagination(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        item_list = ItemFactory.batch(size=2)
        mock_item_repository.get_all.return_value = item_list

        result = item_service.get_all_items(skip=5, limit=15)

        assert len(result) == 2
        mock_item_repository.get_all.assert_called_once_with(5, 15)

    def test_update_item_success(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        existing_item = ItemFactory.potion()
        updated_item = ItemFactory.build(id=1, name="Updated Potion", price=300)
        update_dto = ItemUpdateDTOFactory.name_only()

        mock_item_repository.get_by_id.return_value = existing_item
        mock_item_repository.update.return_value = updated_item

        result = item_service.update_item(1, update_dto)

        assert result is not None
        assert result.name == updated_item.name
        mock_item_repository.get_by_id.assert_called_once_with(1)
        mock_item_repository.update.assert_called_once()

    def test_update_item_price_only(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        existing_item = ItemFactory.potion()
        updated_item = ItemFactory.build(id=1, name="Potion", price=1500)
        update_dto = ItemUpdateDTOFactory.price_only()

        mock_item_repository.get_by_id.return_value = existing_item
        mock_item_repository.update.return_value = updated_item

        result = item_service.update_item(1, update_dto)

        assert result is not None
        assert result.price == 1500
        mock_item_repository.update.assert_called_once()

    def test_update_item_full_update(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        existing_item = ItemFactory.potion()
        updated_item = ItemFactory.build(
            id=1,
            name="Completely Updated Item",
            type=ItemType.STONE,
            price=5000,
        )
        update_dto = ItemUpdateDTOFactory.full_update()

        mock_item_repository.get_by_id.return_value = existing_item
        mock_item_repository.update.return_value = updated_item

        result = item_service.update_item(1, update_dto)

        assert result is not None
        assert result.name == "Completely Updated Item"
        assert result.type == ItemType.STONE.value
        assert result.price == 5000

    def test_update_item_not_found(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        update_dto = ItemUpdateDTOFactory.name_only()
        mock_item_repository.get_by_id.return_value = None

        result = item_service.update_item(999, update_dto)

        assert result is None
        mock_item_repository.get_by_id.assert_called_once_with(999)
        mock_item_repository.update.assert_not_called()

    def test_update_item_negative_price_fails(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        existing_item = ItemFactory.potion()
        mock_item_repository.get_by_id.return_value = existing_item

        updated_item_with_negative_price = ItemFactory.build(id=1, price=-50)

        with pytest.raises(BusinessRuleException, match="Item price cannot be negative"):
            item_service._validate_business_rules_for_update(updated_item_with_negative_price)

    def test_update_item_empty_name_fails(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        existing_item = ItemFactory.potion()
        mock_item_repository.get_by_id.return_value = existing_item

        updated_item_with_empty_name = ItemFactory.build(id=1, name="")

        with pytest.raises(BusinessRuleException, match="Item name cannot be empty"):
            item_service._validate_business_rules_for_update(updated_item_with_empty_name)

    def test_delete_item_success(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        mock_item_repository.delete.return_value = True

        result = item_service.delete_item(1)

        assert result is True
        mock_item_repository.delete.assert_called_once_with(1)

    def test_delete_item_failure(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        mock_item_repository.delete.return_value = False

        result = item_service.delete_item(1)

        assert result is False
        mock_item_repository.delete.assert_called_once_with(1)

    def test_get_items_by_type(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        potion_items = [ItemFactory.potion(), ItemFactory.build(type=ItemType.POTION)]
        mock_item_repository.get_by_type.return_value = potion_items

        result = item_service.get_items_by_type("potion")

        assert len(result) == 2
        for item_dto in result:
            assert item_dto.type == ItemType.POTION.value
        mock_item_repository.get_by_type.assert_called_once_with("potion")

    def test_get_items_by_type_empty(
        self, item_service: ItemService, mock_item_repository: Mock
    ) -> None:
        mock_item_repository.get_by_type.return_value = []

        result = item_service.get_items_by_type("nonexistent")

        assert len(result) == 0
        mock_item_repository.get_by_type.assert_called_once_with("nonexistent")

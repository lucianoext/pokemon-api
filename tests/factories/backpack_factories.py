from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from src.application.dtos.backpack_dto import (
    BackpackAddItemDTO,
    BackpackItemResponseDTO,
    BackpackRemoveItemDTO,
    BackpackResponseDTO,
    BackpackUpdateQuantityDTO,
)
from src.domain.entities.backpack import Backpack


class BackpackFactory(DataclassFactory[Backpack]):
    __model__ = Backpack

    @classmethod
    def ash_potion_entry(cls) -> Backpack:
        return cls.build(
            id=1,
            trainer_id=1,
            item_id=1,
            quantity=5,
        )

    @classmethod
    def ash_pokeball_entry(cls) -> Backpack:
        return cls.build(
            id=2,
            trainer_id=1,
            item_id=2,
            quantity=10,
        )

    @classmethod
    def gary_antidote_entry(cls) -> Backpack:
        return cls.build(
            id=3,
            trainer_id=2,
            item_id=3,
            quantity=3,
        )

    @classmethod
    def single_item_entry(cls) -> Backpack:
        return cls.build(
            trainer_id=1,
            item_id=4,
            quantity=1,
        )

    @classmethod
    def large_quantity_entry(cls) -> Backpack:
        return cls.build(
            trainer_id=1,
            item_id=5,
            quantity=99,
        )

    @classmethod
    def zero_quantity_entry(cls) -> Backpack:
        return cls.build(quantity=0)

    @classmethod
    def negative_quantity_entry(cls) -> Backpack:
        return cls.build(quantity=-1)


class BackpackAddItemDTOFactory(ModelFactory[BackpackAddItemDTO]):
    __model__ = BackpackAddItemDTO

    @classmethod
    def add_potion_to_ash(cls) -> BackpackAddItemDTO:
        return cls.build(
            trainer_id=1,
            item_id=1,
            quantity=5,
        )

    @classmethod
    def add_pokeball_to_ash(cls) -> BackpackAddItemDTO:
        return cls.build(
            trainer_id=1,
            item_id=2,
            quantity=10,
        )

    @classmethod
    def add_single_item(cls) -> BackpackAddItemDTO:
        return cls.build(
            trainer_id=1,
            item_id=3,
            quantity=1,
        )

    @classmethod
    def add_large_quantity(cls) -> BackpackAddItemDTO:
        return cls.build(
            trainer_id=1,
            item_id=4,
            quantity=50,
        )

    @classmethod
    def add_zero_quantity(cls) -> BackpackAddItemDTO:
        return cls.build(
            trainer_id=1,
            item_id=1,
            quantity=0,
        )

    @classmethod
    def add_negative_quantity(cls) -> BackpackAddItemDTO:
        return cls.build(
            trainer_id=1,
            item_id=1,
            quantity=-5,
        )

    @classmethod
    def nonexistent_trainer(cls) -> BackpackAddItemDTO:
        return cls.build(
            trainer_id=999,
            item_id=1,
            quantity=1,
        )

    @classmethod
    def nonexistent_item(cls) -> BackpackAddItemDTO:
        return cls.build(
            trainer_id=1,
            item_id=999,
            quantity=1,
        )


class BackpackRemoveItemDTOFactory(ModelFactory[BackpackRemoveItemDTO]):
    __model__ = BackpackRemoveItemDTO

    @classmethod
    def remove_one(cls) -> BackpackRemoveItemDTO:
        return cls.build(quantity=1)

    @classmethod
    def remove_five(cls) -> BackpackRemoveItemDTO:
        return cls.build(quantity=5)

    @classmethod
    def remove_all(cls) -> BackpackRemoveItemDTO:
        return cls.build(quantity=10)

    @classmethod
    def remove_more_than_available(cls) -> BackpackRemoveItemDTO:
        return cls.build(quantity=20)

    @classmethod
    def remove_zero(cls) -> BackpackRemoveItemDTO:
        return cls.build(quantity=0)

    @classmethod
    def remove_negative(cls) -> BackpackRemoveItemDTO:
        return cls.build(quantity=-3)


class BackpackUpdateQuantityDTOFactory(ModelFactory[BackpackUpdateQuantityDTO]):
    __model__ = BackpackUpdateQuantityDTO

    @classmethod
    def update_to_ten(cls) -> BackpackUpdateQuantityDTO:
        return cls.build(new_quantity=10)

    @classmethod
    def update_to_one(cls) -> BackpackUpdateQuantityDTO:
        return cls.build(new_quantity=1)

    @classmethod
    def update_to_zero(cls) -> BackpackUpdateQuantityDTO:
        return cls.build(new_quantity=0)

    @classmethod
    def update_to_negative(cls) -> BackpackUpdateQuantityDTO:
        return cls.build(new_quantity=-5)

    @classmethod
    def update_to_large_number(cls) -> BackpackUpdateQuantityDTO:
        return cls.build(new_quantity=999)


class BackpackItemResponseDTOFactory(ModelFactory[BackpackItemResponseDTO]):
    __model__ = BackpackItemResponseDTO

    @classmethod
    def potion_item(cls) -> BackpackItemResponseDTO:
        return cls.build(
            id=1,
            trainer_id=1,
            item_id=1,
            item_name="Potion",
            item_type="potion",
            item_description="Restores 20 HP",
            item_price=200,
            quantity=5,
        )

    @classmethod
    def pokeball_item(cls) -> BackpackItemResponseDTO:
        return cls.build(
            id=2,
            trainer_id=1,
            item_id=2,
            item_name="Poke Ball",
            item_type="pokeball",
            item_description="A device for catching wild Pokemon",
            item_price=200,
            quantity=10,
        )

    @classmethod
    def antidote_item(cls) -> BackpackItemResponseDTO:
        return cls.build(
            id=3,
            trainer_id=2,
            item_id=3,
            item_name="Antidote",
            item_type="antidote",
            item_description="Cures poison",
            item_price=100,
            quantity=3,
        )

    @classmethod
    def single_quantity_item(cls) -> BackpackItemResponseDTO:
        return cls.build(quantity=1)

    @classmethod
    def zero_quantity_item(cls) -> BackpackItemResponseDTO:
        return cls.build(quantity=0)


class BackpackResponseDTOFactory(ModelFactory[BackpackResponseDTO]):
    __model__ = BackpackResponseDTO

    @classmethod
    def ash_backpack_empty(cls) -> BackpackResponseDTO:
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            total_items=0,
            items=[],
        )

    @classmethod
    def ash_backpack_with_potion(cls) -> BackpackResponseDTO:
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            total_items=1,
            items=[BackpackItemResponseDTOFactory.potion_item()],
        )

    @classmethod
    def ash_backpack_with_multiple_items(cls) -> BackpackResponseDTO:
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            total_items=2,
            items=[
                BackpackItemResponseDTOFactory.potion_item(),
                BackpackItemResponseDTOFactory.pokeball_item(),
            ],
        )

    @classmethod
    def gary_backpack_empty(cls) -> BackpackResponseDTO:
        return cls.build(
            trainer_id=2,
            trainer_name="Gary Oak",
            total_items=0,
            items=[],
        )

    @classmethod
    def full_backpack(cls) -> BackpackResponseDTO:
        items = [
            BackpackItemResponseDTOFactory.build(
                id=i,
                trainer_id=1,
                item_id=i,
                item_name=f"Item{i}",
                item_type="potion",
                item_description=f"Description for item {i}",
                item_price=100 * i,
                quantity=i * 2,
            )
            for i in range(1, 6)
        ]
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            total_items=5,
            items=items,
        )

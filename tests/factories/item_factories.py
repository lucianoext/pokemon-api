from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from src.application.dtos.item_dto import (
    ItemCreateDTO,
    ItemResponseDTO,
    ItemUpdateDTO,
)
from src.domain.entities.item import Item
from src.domain.enums.item_enums import ItemType


class ItemFactory(DataclassFactory[Item]):
    __model__ = Item

    @classmethod
    def potion(cls) -> Item:
        return cls.build(
            id=1,
            name="Potion",
            type=ItemType.POTION,
            description="Restores 20 HP",
            price=200,
        )

    @classmethod
    def master_ball(cls) -> Item:
        return cls.build(
            id=2,
            name="Master Ball",
            type=ItemType.POKEBALL,
            description="Catches any Pokemon without fail",
            price=100000,
        )

    @classmethod
    def antidote(cls) -> Item:
        return cls.build(
            id=3,
            name="Antidote",
            type=ItemType.ANTIDOTE,
            description="Cures poison",
            price=100,
        )

    @classmethod
    def free_berry(cls) -> Item:
        return cls.build(
            name="Oran Berry",
            type=ItemType.BERRY,
            description="Restores 10 HP when consumed",
            price=0,
        )

    @classmethod
    def expensive_stone(cls) -> Item:
        return cls.build(
            name="Moon Stone",
            type=ItemType.STONE,
            description="Makes certain Pokemon evolve",
            price=cls.__faker__.random_int(min=50000, max=100000),
        )

    @classmethod
    def tm_item(cls) -> Item:
        return cls.build(
            name="TM01 - Focus Punch",
            type=ItemType.TM,
            description="Teaches a Pokemon Focus Punch",
            price=3000,
        )

    @classmethod
    def negative_price_item(cls) -> Item:
        return cls.build(price=-100)

    @classmethod
    def empty_name_item(cls) -> Item:
        return cls.build(name="")


class ItemCreateDTOFactory(ModelFactory[ItemCreateDTO]):
    __model__ = ItemCreateDTO

    @classmethod
    def super_potion(cls) -> ItemCreateDTO:
        return cls.build(
            name="Super Potion",
            type=ItemType.POTION,
            description="Restores 50 HP",
            price=700,
        )

    @classmethod
    def pokeball(cls) -> ItemCreateDTO:
        return cls.build(
            name="Poke Ball",
            type=ItemType.POKEBALL,
            description="A device for catching wild Pokemon",
            price=200,
        )

    @classmethod
    def revive(cls) -> ItemCreateDTO:
        return cls.build(
            name="Revive",
            type=ItemType.REVIVE,
            description="Revives a fainted Pokemon with half HP",
            price=1500,
        )

    @classmethod
    def negative_price(cls) -> ItemCreateDTO:
        return cls.build(
            name="Invalid Item",
            type=ItemType.POTION,
            description="This item has negative price",
            price=-100,
        )

    @classmethod
    def empty_name(cls) -> ItemCreateDTO:
        return cls.build(
            name="",
            type=ItemType.BERRY,
            description="Item with empty name",
            price=50,
        )

    @classmethod
    def free_item(cls) -> ItemCreateDTO:
        return cls.build(
            name="Free Berry",
            type=ItemType.BERRY,
            description="A free berry",
            price=0,
        )


class ItemUpdateDTOFactory(ModelFactory[ItemUpdateDTO]):
    __model__ = ItemUpdateDTO

    @classmethod
    def name_only(cls) -> ItemUpdateDTO:
        return cls.build(
            name="Updated Item Name",
            type=None,
            description=None,
            price=None,
        )

    @classmethod
    def price_only(cls) -> ItemUpdateDTO:
        return cls.build(
            name=None,
            type=None,
            description=None,
            price=1500,
        )

    @classmethod
    def type_and_description(cls) -> ItemUpdateDTO:
        return cls.build(
            name=None,
            type=ItemType.TM,
            description="Updated to be a TM item",
            price=None,
        )

    @classmethod
    def full_update(cls) -> ItemUpdateDTO:
        return cls.build(
            name="Completely Updated Item",
            type=ItemType.STONE,
            description="This item has been completely updated",
            price=5000,
        )

    @classmethod
    def negative_price_update(cls) -> ItemUpdateDTO:
        return cls.build(
            name=None,
            type=None,
            description=None,
            price=-50,
        )

    @classmethod
    def empty_name_update(cls) -> ItemUpdateDTO:
        return cls.build(
            name="",
            type=None,
            description=None,
            price=None,
        )


class ItemResponseDTOFactory(ModelFactory[ItemResponseDTO]):
    __model__ = ItemResponseDTO

    @classmethod
    def from_item(cls, item: Item) -> ItemResponseDTO:
        return cls.build(
            id=item.id,
            name=item.name,
            type=item.type.value,
            description=item.description,
            price=item.price,
        )

    @classmethod
    def potion_response(cls) -> ItemResponseDTO:
        return cls.build(
            id=1,
            name="Potion",
            type=ItemType.POTION.value,
            description="Restores 20 HP",
            price=200,
        )

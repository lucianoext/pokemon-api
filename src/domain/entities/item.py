from dataclasses import dataclass

from src.domain.enums.item_enums import ItemType


@dataclass
class Item:
    id: int | None
    name: str
    type: ItemType
    description: str | None = ""
    price: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.type, str):
            self.type = ItemType(self.type)

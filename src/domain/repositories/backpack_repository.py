from abc import ABC, abstractmethod

from ..entities.backpack import Backpack


class BackpackRepository(ABC):
    @abstractmethod
    def add_item(self, backpack: Backpack) -> Backpack:
        pass

    @abstractmethod
    def remove_item(self, trainer_id: int, item_id: int, quantity: int) -> bool:
        pass

    @abstractmethod
    def get_trainer_backpack(self, trainer_id: int) -> list[Backpack]:
        pass

    @abstractmethod
    def get_item_quantity(self, trainer_id: int, item_id: int) -> int:
        pass

    @abstractmethod
    def update_quantity(
        self, trainer_id: int, item_id: int, new_quantity: int
    ) -> Backpack | None:
        pass

    @abstractmethod
    def clear_backpack(self, trainer_id: int) -> bool:
        pass

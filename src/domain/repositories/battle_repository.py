from abc import ABC, abstractmethod

from ..entities.battle import Battle


class BattleRepository(ABC):
    @abstractmethod
    def create_battle(self, battle: Battle) -> Battle:
        pass

    @abstractmethod
    def get_by_id(self, battle_id: int) -> Battle | None:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Battle]:
        pass

    @abstractmethod
    def get_battles_by_trainer(self, trainer_id: int) -> list[Battle]:
        pass

    @abstractmethod
    def get_trainer_wins(self, trainer_id: int) -> int:
        pass

    @abstractmethod
    def get_trainer_losses(self, trainer_id: int) -> int:
        pass

    @abstractmethod
    def get_leaderboard_data(self) -> list[dict]:
        pass

    @abstractmethod
    def delete_battle(self, battle_id: int) -> bool:
        pass

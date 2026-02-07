from abc import ABC, abstractmethod

from src.domain.repositories.base_repository import BaseRepository

from ..entities.battle import Battle


class BattleRepository(BaseRepository[Battle], ABC):
    @abstractmethod
    def create_battle(self, battle: Battle) -> Battle:
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

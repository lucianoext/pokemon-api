from abc import ABC

from src.domain.repositories.base_repository import BaseRepository

from ..entities.trainer import Trainer


class TrainerRepository(BaseRepository[Trainer], ABC):
    pass

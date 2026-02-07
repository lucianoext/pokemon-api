from abc import ABC, abstractmethod

from src.domain.repositories.base_repository import BaseRepository

from ..entities.user import User


class UserRepository(BaseRepository[User], ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

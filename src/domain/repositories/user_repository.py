from abc import ABC, abstractmethod

from ..entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        pass

    @abstractmethod
    def update(self, user_id: int, user: User) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

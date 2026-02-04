from datetime import datetime

from sqlmodel import Session, select

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.persistence.database.models import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            trainer_id=user.trainer_id,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return self._model_to_entity(db_user)

    def get_by_id(self, user_id: int) -> User | None:
        db_user = self.db.get(UserModel, user_id)
        return self._model_to_entity(db_user) if db_user else None

    def get_by_username(self, username: str) -> User | None:
        statement = select(UserModel).where(UserModel.username == username)
        db_user = self.db.exec(statement).first()
        return self._model_to_entity(db_user) if db_user else None

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        db_user = self.db.exec(statement).first()
        return self._model_to_entity(db_user) if db_user else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        statement = select(UserModel).offset(skip).limit(limit)
        db_users = self.db.exec(statement).all()
        return [self._model_to_entity(user) for user in db_users]

    def update(self, user_id: int, user: User) -> User | None:
        db_user = self.db.get(UserModel, user_id)
        if not db_user:
            return None

        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = user.hashed_password
        db_user.is_active = user.is_active
        db_user.is_superuser = user.is_superuser
        db_user.trainer_id = user.trainer_id
        db_user.updated_at = datetime.utcnow()

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return self._model_to_entity(db_user)

    def delete(self, user_id: int) -> bool:
        db_user = self.db.get(UserModel, user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            is_superuser=model.is_superuser,
            created_at=model.created_at,
            updated_at=model.updated_at,
            trainer_id=model.trainer_id,
        )

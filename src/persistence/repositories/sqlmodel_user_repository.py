from datetime import datetime

from sqlmodel import Session, select

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.persistence.database.models import UserModel
from src.persistence.repositories.base_sqlmodel_repository import BaseSqlModelRepository


class SqlModelUserRepository(BaseSqlModelRepository[User, UserModel], UserRepository):
    """SQLModel-based User repository with generics."""

    def __init__(self, db: Session):
        super().__init__(
            db=db,
            model_class=UserModel,
            entity_to_model_mapper=self._entity_to_model,
            model_to_entity_mapper=self._model_to_entity,
        )

    def _entity_to_model(self, user: User) -> UserModel:
        """Convert User entity to SQLModel."""
        return UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
            trainer_id=user.trainer_id,
        )

    def _model_to_entity(self, model: UserModel) -> User:
        """Convert SQLModel to User entity."""
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

    # Domain-specific methods
    def get_by_username(self, username: str) -> User | None:
        """Get user by username - custom query."""
        statement = select(UserModel).where(UserModel.username == username)
        db_user = self.db.exec(statement).first()
        return self._model_to_entity(db_user) if db_user else None

    def get_by_email(self, email: str) -> User | None:
        """Get user by email - custom query."""
        statement = select(UserModel).where(UserModel.email == email)
        db_user = self.db.exec(statement).first()
        return self._model_to_entity(db_user) if db_user else None

    def update(self, user_id: int, user: User) -> User | None:
        """Update user with timestamp - custom logic."""
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

from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.application.dtos.auth_dto import (
    ChangePasswordDTO,
    LoginResponseDTO,
    TokenResponseDTO,
    UserLoginDTO,
    UserRegistrationDTO,
    UserResponseDTO,
)
from src.config import settings
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _hash_password(self, password: str) -> str:
        return str(self.pwd_context.hash(password))

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bool(self.pwd_context.verify(plain_password, hashed_password))

    def _create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire, "type": "access"})

        return str(
            jwt.encode(
                to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
            )
        )

    def register_user(self, user_data: UserRegistrationDTO) -> UserResponseDTO:
        existing_user = self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise ValueError("Username already exists")

        existing_email = self.user_repository.get_by_email(user_data.email)
        if existing_email:
            raise ValueError("Email already exists")

        user = User(
            id=None,
            username=user_data.username,
            email=user_data.email,
            hashed_password=self._hash_password(user_data.password),
        )

        created_user = self.user_repository.create(user)

        return UserResponseDTO(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            is_active=created_user.is_active,
            is_superuser=created_user.is_superuser,
            created_at=created_user.created_at or datetime.utcnow(),
            trainer_id=created_user.trainer_id,
        )

    def authenticate_user(self, login_data: UserLoginDTO) -> LoginResponseDTO:
        user = self.user_repository.get_by_username(login_data.username)

        if not user or not self._verify_password(
            login_data.password, user.hashed_password
        ):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User account is inactive")

        access_token = self._create_access_token(
            {
                "sub": str(user.id),
                "username": user.username,
                "email": user.email,
                "is_superuser": user.is_superuser,
            }
        )

        tokens = TokenResponseDTO(
            access_token=access_token,
            refresh_token="temp_refresh_token",  # nosec B106
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        user_response = UserResponseDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at or datetime.utcnow(),
            trainer_id=user.trainer_id,
        )

        return LoginResponseDTO(user=user_response, tokens=tokens)

    def get_current_user_from_token(self, token: str) -> User | None:  # UP045
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get("sub")

            if user_id is None:
                return None

            return self.user_repository.get_by_id(int(user_id))

        except JWTError:
            return None

    def change_password(self, user_id: int, password_data: ChangePasswordDTO) -> bool:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if not self._verify_password(
            password_data.current_password, user.hashed_password
        ):
            raise ValueError("Current password is incorrect")

        user.hashed_password = self._hash_password(password_data.new_password)
        self.user_repository.update(user_id, user)

        return True

from datetime import datetime, timedelta
from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from src.application.dtos.auth_dto import (
    ChangePasswordDTO,
    LoginResponseDTO,
    MessageResponseDTO,
    TokenResponseDTO,
    UserLoginDTO,
    UserRegistrationDTO,
    UserResponseDTO,
)
from src.domain.entities.user import User


class UserFactory(DataclassFactory[User]):
    __model__ = User

    @classmethod
    def ash_user(cls) -> User:
        return cls.build(
            id=1,
            username="ash_ketchum",
            email="ash@pokemon.com",
            hashed_password="$2b$12$hashed_password_ash",
            is_active=True,
            is_superuser=False,
            created_at=datetime(2024, 1, 1, 10, 0, 0),
            updated_at=None,
            trainer_id=1,
        )

    @classmethod
    def gary_user(cls) -> User:
        return cls.build(
            id=2,
            username="gary_oak",
            email="gary@pokemon.com",
            hashed_password="$2b$12$hashed_password_gary",
            is_active=True,
            is_superuser=False,
            created_at=datetime(2024, 1, 2, 11, 0, 0),
            updated_at=None,
            trainer_id=2,
        )

    @classmethod
    def admin_user(cls) -> User:
        return cls.build(
            id=3,
            username="admin",
            email="admin@pokemon.com",
            hashed_password="$2b$12$hashed_password_admin",
            is_active=True,
            is_superuser=True,
            created_at=datetime(2024, 1, 1, 9, 0, 0),
            updated_at=None,
            trainer_id=None,
        )

    @classmethod
    def inactive_user(cls) -> User:
        return cls.build(
            id=4,
            username="inactive_user",
            email="inactive@pokemon.com",
            hashed_password="$2b$12$hashed_password_inactive",
            is_active=False,
            is_superuser=False,
            created_at=datetime(2024, 1, 3, 12, 0, 0),
            trainer_id=None,
        )

    @classmethod
    def new_user(cls) -> User:
        return cls.build(
            id=None,
            username="new_user",
            email="newuser@pokemon.com",
            hashed_password="$2b$12$hashed_password_new",
            is_active=True,
            is_superuser=False,
            created_at=None,
            trainer_id=None,
        )


class UserRegistrationDTOFactory(ModelFactory[UserRegistrationDTO]):
    __model__ = UserRegistrationDTO

    @classmethod
    def ash_registration(cls) -> UserRegistrationDTO:
        return cls.build(
            username="ash_ketchum",
            email="ash@pokemon.com",
            password="pikachu123",
            trainer_name="Ash Ketchum",
            trainer_gender="male",
            trainer_region="kanto",
        )

    @classmethod
    def gary_registration(cls) -> UserRegistrationDTO:
        return cls.build(
            username="gary_oak",
            email="gary@pokemon.com",
            password="rival456",
            trainer_name="Gary Oak",
            trainer_gender="male",
            trainer_region="kanto",
        )

    @classmethod
    def simple_registration(cls) -> UserRegistrationDTO:
        return cls.build(
            username="simple_user",
            email="simple@pokemon.com",
            password="password123",
            trainer_name=None,
            trainer_gender=None,
            trainer_region=None,
        )

    @classmethod
    def invalid_short_password(cls) -> UserRegistrationDTO:
        return cls.build(
            username="test_user",
            email="test@pokemon.com",
            password="123",
        )

    @classmethod
    def invalid_short_username(cls) -> UserRegistrationDTO:
        return cls.build(
            username="ab",
            email="test@pokemon.com",
            password="password123",
        )

    @classmethod
    def existing_username(cls) -> UserRegistrationDTO:
        return cls.build(
            username="ash_ketchum",
            email="different@pokemon.com",
            password="password123",
        )

    @classmethod
    def existing_email(cls) -> UserRegistrationDTO:
        return cls.build(
            username="different_user",
            email="ash@pokemon.com",
            password="password123",
        )


class UserLoginDTOFactory(ModelFactory[UserLoginDTO]):
    __model__ = UserLoginDTO

    @classmethod
    def ash_login(cls) -> UserLoginDTO:
        return cls.build(
            username="ash_ketchum",
            password="pikachu123",
        )

    @classmethod
    def gary_login(cls) -> UserLoginDTO:
        return cls.build(
            username="gary_oak",
            password="rival456",
        )

    @classmethod
    def admin_login(cls) -> UserLoginDTO:
        return cls.build(
            username="admin",
            password="admin123",
        )

    @classmethod
    def invalid_credentials(cls) -> UserLoginDTO:
        return cls.build(
            username="ash_ketchum",
            password="wrong_password",
        )

    @classmethod
    def nonexistent_user(cls) -> UserLoginDTO:
        return cls.build(
            username="nonexistent",
            password="password123",
        )

    @classmethod
    def inactive_user_login(cls) -> UserLoginDTO:
        return cls.build(
            username="inactive_user",
            password="password123",
        )


class TokenResponseDTOFactory(ModelFactory[TokenResponseDTO]):
    __model__ = TokenResponseDTO

    @classmethod
    def valid_token(cls) -> TokenResponseDTO:
        return cls.build(
            access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.sample.token",
            refresh_token="sample_refresh_token",
            token_type="bearer",
            expires_in=3600,
        )

    @classmethod
    def expired_token(cls) -> TokenResponseDTO:
        return cls.build(
            access_token="expired.jwt.token",
            refresh_token="expired_refresh_token",
            token_type="bearer",
            expires_in=0,
        )


class UserResponseDTOFactory(ModelFactory[UserResponseDTO]):
    __model__ = UserResponseDTO

    @classmethod
    def from_user(cls, user: User) -> UserResponseDTO:
        return cls.build(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at or datetime.utcnow(),
            trainer_id=user.trainer_id,
        )

    @classmethod
    def ash_response(cls) -> UserResponseDTO:
        return cls.build(
            id=1,
            username="ash_ketchum",
            email="ash@pokemon.com",
            is_active=True,
            is_superuser=False,
            created_at=datetime(2024, 1, 1, 10, 0, 0),
            trainer_id=1,
        )

    @classmethod
    def admin_response(cls) -> UserResponseDTO:
        return cls.build(
            id=3,
            username="admin",
            email="admin@pokemon.com",
            is_active=True,
            is_superuser=True,
            created_at=datetime(2024, 1, 1, 9, 0, 0),
            trainer_id=None,
        )


class LoginResponseDTOFactory(ModelFactory[LoginResponseDTO]):
    __model__ = LoginResponseDTO

    @classmethod
    def ash_login_success(cls) -> LoginResponseDTO:
        return cls.build(
            user=UserResponseDTOFactory.ash_response(),
            tokens=TokenResponseDTOFactory.valid_token(),
            message="Login successful",
        )

    @classmethod
    def admin_login_success(cls) -> LoginResponseDTO:
        return cls.build(
            user=UserResponseDTOFactory.admin_response(),
            tokens=TokenResponseDTOFactory.valid_token(),
            message="Login successful",
        )


class ChangePasswordDTOFactory(ModelFactory[ChangePasswordDTO]):
    __model__ = ChangePasswordDTO

    @classmethod
    def valid_change(cls) -> ChangePasswordDTO:
        return cls.build(
            current_password="pikachu123",
            new_password="newpassword456",
        )

    @classmethod
    def wrong_current_password(cls) -> ChangePasswordDTO:
        return cls.build(
            current_password="wrong_password",
            new_password="newpassword456",
        )

    @classmethod
    def weak_new_password(cls) -> ChangePasswordDTO:
        return cls.build(
            current_password="pikachu123",
            new_password="123",
        )


class MessageResponseDTOFactory(ModelFactory[MessageResponseDTO]):
    __model__ = MessageResponseDTO

    @classmethod
    def success(cls) -> MessageResponseDTO:
        return cls.build(message="Operation completed successfully")

    @classmethod
    def error(cls) -> MessageResponseDTO:
        return cls.build(message="An error occurred")

    @classmethod
    def password_changed(cls) -> MessageResponseDTO:
        return cls.build(message="Password changed successfully")

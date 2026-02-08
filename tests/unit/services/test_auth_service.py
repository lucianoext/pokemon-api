from unittest.mock import Mock, patch
import pytest
import sys
from datetime import datetime


class MockSettings:
    JWT_SECRET_KEY = "test_secret_key"
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30


class MockCryptContext:
    def __init__(self, schemes, deprecated):
        pass

    def hash(self, password):
        return f"$2b$12$hashed_{password}"

    def verify(self, plain_password, hashed_password):
        return plain_password in hashed_password


class MockJWT:
    @staticmethod
    def encode(data, secret, algorithm):
        return f"mock_token_{data.get('sub', 'unknown')}"

    @staticmethod
    def decode(token, secret, algorithms):
        if token == "invalid_token":
            raise MockJWTError("Invalid token")
        return {"sub": "1", "username": "test_user"}


class MockJWTError(Exception):
    pass


class TestAuthService:

    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        modules_to_mock = {
            'jose': Mock(),
            'jose.jwt': MockJWT(),
            'jose.JWTError': MockJWTError,
            'passlib': Mock(),
            'passlib.context': Mock(),
            'src.config': Mock(settings=MockSettings()),
            'pydantic_settings': Mock(),
            'dotenv': Mock(),
        }

        with patch.dict('sys.modules', modules_to_mock):
            with patch('jose.jwt', MockJWT), \
                 patch('jose.JWTError', MockJWTError), \
                 patch('passlib.context.CryptContext', MockCryptContext):
                yield

    @pytest.fixture
    def mock_user_repository(self):
        return Mock()

    @pytest.fixture
    def auth_service(self, mock_user_repository):
        with patch('src.application.services.auth_service.settings', MockSettings):
            from src.application.services.auth_service import AuthService
            return AuthService(user_repository=mock_user_repository)

    def test_hash_password(self, auth_service):
        result = auth_service._hash_password("test_password")

        assert result.startswith("$2b$12$hashed_")
        assert "test_password" in result

    def test_verify_password_correct(self, auth_service):
        password = "test_password"
        hashed = auth_service._hash_password(password)

        result = auth_service._verify_password(password, hashed)

        assert result is True

    def test_verify_password_incorrect(self, auth_service):
        hashed = auth_service._hash_password("correct_password")

        result = auth_service._verify_password("wrong_password", hashed)

        assert result is False

    def test_create_access_token(self, auth_service):
        data = {"sub": "123", "username": "test_user"}

        token = auth_service._create_access_token(data)

        assert token == "mock_token_123"

    def test_register_user_success(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import UserRegistrationDTOFactory, UserFactory

        registration_dto = UserRegistrationDTOFactory.ash_registration()
        created_user = UserFactory.ash_user()

        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.create.return_value = created_user

        result = auth_service.register_user(registration_dto)

        assert result.username == "ash_ketchum"
        assert result.email == "ash@pokemon.com"
        assert result.is_active is True
        mock_user_repository.create.assert_called_once()

    def test_register_user_username_exists(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import UserRegistrationDTOFactory, UserFactory

        registration_dto = UserRegistrationDTOFactory.existing_username()
        existing_user = UserFactory.ash_user()

        mock_user_repository.get_by_username.return_value = existing_user

        with pytest.raises(ValueError, match="Username already exists"):
            auth_service.register_user(registration_dto)

    def test_register_user_email_exists(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import UserRegistrationDTOFactory, UserFactory

        registration_dto = UserRegistrationDTOFactory.existing_email()
        existing_user = UserFactory.ash_user()

        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.get_by_email.return_value = existing_user

        with pytest.raises(ValueError, match="Email already exists"):
            auth_service.register_user(registration_dto)

    def test_authenticate_user_success(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import UserLoginDTOFactory, UserFactory

        login_dto = UserLoginDTOFactory.ash_login()
        user = UserFactory.ash_user()
        user.hashed_password = auth_service._hash_password("pikachu123")

        mock_user_repository.get_by_username.return_value = user

        result = auth_service.authenticate_user(login_dto)

        assert result.user.username == "ash_ketchum"
        assert result.user.email == "ash@pokemon.com"
        assert result.tokens.access_token is not None
        assert result.tokens.token_type == "bearer"

    def test_authenticate_user_invalid_credentials(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import UserLoginDTOFactory, UserFactory

        login_dto = UserLoginDTOFactory.invalid_credentials()
        user = UserFactory.ash_user()
        user.hashed_password = auth_service._hash_password("correct_password")

        mock_user_repository.get_by_username.return_value = user

        with pytest.raises(ValueError, match="Invalid credentials"):
            auth_service.authenticate_user(login_dto)

    def test_authenticate_user_not_found(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import UserLoginDTOFactory

        login_dto = UserLoginDTOFactory.nonexistent_user()
        mock_user_repository.get_by_username.return_value = None

        with pytest.raises(ValueError, match="Invalid credentials"):
            auth_service.authenticate_user(login_dto)

    def test_authenticate_user_inactive(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import UserLoginDTOFactory, UserFactory

        login_dto = UserLoginDTOFactory.inactive_user_login()
        user = UserFactory.inactive_user()
        user.hashed_password = auth_service._hash_password("password123")

        mock_user_repository.get_by_username.return_value = user

        with pytest.raises(ValueError, match="User account is inactive"):
            auth_service.authenticate_user(login_dto)

    def test_get_current_user_from_token_success(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import UserFactory

        user = UserFactory.ash_user()
        token = "valid_token"

        mock_user_repository.get_by_id.return_value = user

        result = auth_service.get_current_user_from_token(token)

        assert result is not None
        assert result.username == "ash_ketchum"
        mock_user_repository.get_by_id.assert_called_once_with(1)

    def test_get_current_user_from_token_invalid(self, auth_service, mock_user_repository):
        result = auth_service.get_current_user_from_token("invalid_token")

        assert result is None
        mock_user_repository.get_by_id.assert_not_called()

    def test_change_password_success(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import ChangePasswordDTOFactory, UserFactory

        user_id = 1
        change_dto = ChangePasswordDTOFactory.valid_change()
        user = UserFactory.ash_user()
        user.hashed_password = auth_service._hash_password("pikachu123")

        mock_user_repository.get_by_id.return_value = user
        mock_user_repository.update.return_value = user

        result = auth_service.change_password(user_id, change_dto)

        assert result is True
        mock_user_repository.update.assert_called_once_with(user_id, user)

    def test_change_password_user_not_found(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import ChangePasswordDTOFactory

        user_id = 999
        change_dto = ChangePasswordDTOFactory.valid_change()
        mock_user_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="User not found"):
            auth_service.change_password(user_id, change_dto)

    def test_change_password_wrong_current_password(self, auth_service, mock_user_repository):
        from tests.factories.auth_factories import ChangePasswordDTOFactory, UserFactory

        user_id = 1
        change_dto = ChangePasswordDTOFactory.wrong_current_password()
        user = UserFactory.ash_user()
        user.hashed_password = auth_service._hash_password("correct_password")

        mock_user_repository.get_by_id.return_value = user

        with pytest.raises(ValueError, match="Current password is incorrect"):
            auth_service.change_password(user_id, change_dto)

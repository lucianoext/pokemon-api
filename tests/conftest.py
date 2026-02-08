from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_pokemon_repository() -> Mock:
    return Mock()


@pytest.fixture
def mock_trainer_repository() -> Mock:
    return Mock()


@pytest.fixture
def mock_item_repository() -> Mock:
    return Mock()


@pytest.fixture
def mock_team_repository() -> Mock:
    return Mock()


@pytest.fixture
def mock_battle_repository() -> Mock:
    return Mock()


@pytest.fixture
def mock_user_repository() -> Mock:
    return Mock()

@pytest.fixture
def mock_backpack_repository() -> Mock:
    return Mock()

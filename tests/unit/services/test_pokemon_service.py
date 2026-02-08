from unittest.mock import Mock

import pytest

from src.application.services.pokemon_service import PokemonService
from src.domain.exceptions import BusinessRuleException
from tests.factories.pokemon_factories import (
    PokemonCreateDTOFactory,
    PokemonFactory,
    PokemonUpdateDTOFactory,
)


class TestPokemonService:
    @pytest.fixture
    def pokemon_service(self, mock_pokemon_repository: Mock) -> PokemonService:
        return PokemonService(pokemon_repository=mock_pokemon_repository)

    def test_create_pokemon_success(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        create_dto = PokemonCreateDTOFactory.charizard()
        pokemon = PokemonFactory.charizard()
        mock_pokemon_repository.create.return_value = pokemon

        result = pokemon_service.create_pokemon(create_dto)

        assert result.name == pokemon.name
        assert result.level == pokemon.level
        assert result.type_primary == pokemon.type_primary.value
        mock_pokemon_repository.create.assert_called_once()

    def test_create_pokemon_invalid_level_high(
        self, pokemon_service: PokemonService
    ) -> None:
        create_dto = PokemonCreateDTOFactory.invalid_level_high()

        with pytest.raises(
            BusinessRuleException, match="Pokemon level must be between 1 and 100"
        ):
            pokemon_service.create_pokemon(create_dto)

    def test_create_pokemon_invalid_level_low(
        self, pokemon_service: PokemonService
    ) -> None:
        create_dto = PokemonCreateDTOFactory.invalid_level_low()

        with pytest.raises(
            BusinessRuleException, match="Pokemon level must be between 1 and 100"
        ):
            pokemon_service.create_pokemon(create_dto)

    def test_create_pokemon_powerful_attack_insufficient_level(
        self, pokemon_service: PokemonService
    ) -> None:
        create_dto = PokemonCreateDTOFactory.with_powerful_attack_low_level()

        with pytest.raises(BusinessRuleException, match="requires level"):
            pokemon_service.create_pokemon(create_dto)

    def test_create_pokemon_high_level_insufficient_attacks(
        self, pokemon_service: PokemonService
    ) -> None:
        create_dto = PokemonCreateDTOFactory.high_level_few_attacks()

        with pytest.raises(
            BusinessRuleException, match="should know at least 3 attacks"
        ):
            pokemon_service.create_pokemon(create_dto)

    def test_create_pokemon_low_level_few_attacks_success(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        create_dto = PokemonCreateDTOFactory.valid_low_level()
        pokemon = PokemonFactory.build()
        mock_pokemon_repository.create.return_value = pokemon

        result = pokemon_service.create_pokemon(create_dto)

        assert result is not None
        mock_pokemon_repository.create.assert_called_once()

    def test_get_pokemon_found(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon = PokemonFactory.pikachu()
        mock_pokemon_repository.get_by_id.return_value = pokemon

        result = pokemon_service.get_pokemon(1)

        assert result is not None
        assert result.id == pokemon.id
        assert result.name == pokemon.name
        mock_pokemon_repository.get_by_id.assert_called_once_with(1)

    def test_get_pokemon_not_found(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        mock_pokemon_repository.get_by_id.return_value = None

        result = pokemon_service.get_pokemon(999)

        assert result is None

    def test_get_all_pokemon_success(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon_list = PokemonFactory.batch(size=3)
        mock_pokemon_repository.get_all.return_value = pokemon_list

        result = pokemon_service.get_all_pokemon(skip=0, limit=10)

        assert len(result) == 3
        mock_pokemon_repository.get_all.assert_called_once_with(0, 10)

    def test_get_all_pokemon_empty_list(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        mock_pokemon_repository.get_all.return_value = []

        result = pokemon_service.get_all_pokemon()

        assert len(result) == 0
        mock_pokemon_repository.get_all.assert_called_once_with(0, 100)

    def test_update_pokemon_success(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        existing_pokemon = PokemonFactory.pikachu()
        updated_pokemon = PokemonFactory.build(id=1, name="Updated Pikachu", level=50)
        update_dto = PokemonUpdateDTOFactory.name_only()

        mock_pokemon_repository.get_by_id.return_value = existing_pokemon
        mock_pokemon_repository.update.return_value = updated_pokemon

        result = pokemon_service.update_pokemon(1, update_dto)

        assert result is not None
        assert result.name == updated_pokemon.name
        mock_pokemon_repository.get_by_id.assert_called_once_with(1)
        mock_pokemon_repository.update.assert_called_once()

    def test_update_pokemon_not_found(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        update_dto = PokemonUpdateDTOFactory.name_only()
        mock_pokemon_repository.get_by_id.return_value = None

        result = pokemon_service.update_pokemon(999, update_dto)

        assert result is None
        mock_pokemon_repository.get_by_id.assert_called_once_with(999)
        mock_pokemon_repository.update.assert_not_called()

    def test_delete_pokemon_success(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        mock_pokemon_repository.delete.return_value = True

        result = pokemon_service.delete_pokemon(1)

        assert result is True
        mock_pokemon_repository.delete.assert_called_once_with(1)

    def test_delete_pokemon_failure(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        mock_pokemon_repository.delete.return_value = False

        result = pokemon_service.delete_pokemon(1)

        assert result is False
        mock_pokemon_repository.delete.assert_called_once_with(1)

    def test_level_up_pokemon_success(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon = PokemonFactory.build(level=25)
        updated_pokemon = PokemonFactory.build(id=pokemon.id, level=26)

        mock_pokemon_repository.get_by_id.return_value = pokemon
        mock_pokemon_repository.update.return_value = updated_pokemon

        result = pokemon_service.level_up_pokemon(1, 1)

        assert result is not None
        assert result.level == 26
        mock_pokemon_repository.update.assert_called_once()

    def test_level_up_pokemon_exceeds_cap(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon = PokemonFactory.max_level()
        mock_pokemon_repository.get_by_id.return_value = pokemon

        with pytest.raises(BusinessRuleException, match="The level cap is 100"):
            pokemon_service.level_up_pokemon(1, 1)

    def test_level_up_pokemon_not_found(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        mock_pokemon_repository.get_by_id.return_value = None

        result = pokemon_service.level_up_pokemon(999, 1)

        assert result is None
        mock_pokemon_repository.get_by_id.assert_called_once_with(999)

    def test_learn_new_attack_success(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon = PokemonFactory.build(attacks=["Thunder Shock", "Quick Attack"])
        mock_pokemon_repository.get_by_id.return_value = pokemon
        mock_pokemon_repository.update.return_value = pokemon

        result = pokemon_service.learn_new_attack(1, "Thunder")

        assert result is not None
        mock_pokemon_repository.update.assert_called_once()

    def test_learn_attack_already_known(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon = PokemonFactory.build(attacks=["Thunder Shock", "Quick Attack"])
        mock_pokemon_repository.get_by_id.return_value = pokemon

        with pytest.raises(BusinessRuleException, match="already knows"):
            pokemon_service.learn_new_attack(1, "Thunder Shock")

    def test_learn_attack_max_capacity(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon = PokemonFactory.with_four_attacks()
        mock_pokemon_repository.get_by_id.return_value = pokemon

        with pytest.raises(BusinessRuleException, match="already knows 4 attacks"):
            pokemon_service.learn_new_attack(1, "Thunder")

    def test_learn_attack_replace_success(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon = PokemonFactory.with_four_attacks()
        mock_pokemon_repository.get_by_id.return_value = pokemon
        mock_pokemon_repository.update.return_value = pokemon

        result = pokemon_service.learn_new_attack(1, "Thunder", "Move 1")

        assert result is not None
        mock_pokemon_repository.update.assert_called_once()

    def test_learn_attack_replace_unknown_move(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        pokemon = PokemonFactory.with_four_attacks()
        mock_pokemon_repository.get_by_id.return_value = pokemon

        with pytest.raises(BusinessRuleException, match="doesn't know"):
            pokemon_service.learn_new_attack(1, "Thunder", "Unknown Move")

    def test_learn_attack_pokemon_not_found(
        self, pokemon_service: PokemonService, mock_pokemon_repository: Mock
    ) -> None:
        mock_pokemon_repository.get_by_id.return_value = None

        result = pokemon_service.learn_new_attack(999, "Thunder")

        assert result is None
        mock_pokemon_repository.get_by_id.assert_called_once_with(999)

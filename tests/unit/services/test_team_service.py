from unittest.mock import Mock, call

import pytest

from src.application.services.team_service import TeamService
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException
from tests.factories.pokemon_factories import PokemonFactory
from tests.factories.team_factories import (
    TeamAddPokemonDTOFactory,
    TeamFactory,
    TeamUpdatePositionDTOFactory,
)
from tests.factories.trainer_factories import TrainerFactory


class TestTeamService:
    @pytest.fixture
    def team_service(
        self,
        mock_team_repository: Mock,
        mock_trainer_repository: Mock,
        mock_pokemon_repository: Mock,
    ) -> TeamService:
        return TeamService(
            team_repository=mock_team_repository,
            trainer_repository=mock_trainer_repository,
            pokemon_repository=mock_pokemon_repository,
        )

    def test_add_pokemon_to_team_success(
        self,
        team_service: TeamService,
        mock_team_repository: Mock,
        mock_trainer_repository: Mock,
        mock_pokemon_repository: Mock,
    ) -> None:
        add_dto = TeamAddPokemonDTOFactory.add_pikachu_to_ash()
        trainer = TrainerFactory.ash_ketchum()
        pokemon = PokemonFactory.pikachu()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_pokemon_repository.get_by_id.return_value = pokemon
        mock_team_repository.get_trainer_team_size.return_value = 0
        mock_team_repository.get_team_member.return_value = None
        mock_team_repository.get_team_by_trainer.return_value = []

        mock_team_repository.add_pokemon_to_team.return_value = None

        result = team_service.add_pokemon_to_team(add_dto)

        assert result.trainer_id == trainer.id
        assert result.trainer_name == trainer.name
        assert result.team_size == 0
        assert mock_trainer_repository.get_by_id.call_count == 2
        mock_trainer_repository.get_by_id.assert_has_calls([call(1), call(1)])
        mock_pokemon_repository.get_by_id.assert_called_once_with(1)
        mock_team_repository.add_pokemon_to_team.assert_called_once()

    def test_add_pokemon_trainer_not_found(
        self,
        team_service: TeamService,
        mock_trainer_repository: Mock,
    ) -> None:
        add_dto = TeamAddPokemonDTOFactory.add_pikachu_to_ash()
        mock_trainer_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Trainer.*1"):
            team_service.add_pokemon_to_team(add_dto)

        mock_trainer_repository.get_by_id.assert_called_once_with(1)

    def test_add_pokemon_pokemon_not_found(
        self,
        team_service: TeamService,
        mock_trainer_repository: Mock,
        mock_pokemon_repository: Mock,
    ) -> None:
        add_dto = TeamAddPokemonDTOFactory.add_pikachu_to_ash()
        trainer = TrainerFactory.ash_ketchum()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_pokemon_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Pokemon.*1"):
            team_service.add_pokemon_to_team(add_dto)

        mock_pokemon_repository.get_by_id.assert_called_once_with(1)

    def test_add_pokemon_team_full(
        self,
        team_service: TeamService,
        mock_trainer_repository: Mock,
        mock_pokemon_repository: Mock,
        mock_team_repository: Mock,
    ) -> None:
        add_dto = TeamAddPokemonDTOFactory.add_pikachu_to_ash()
        trainer = TrainerFactory.ash_ketchum()
        pokemon = PokemonFactory.pikachu()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_pokemon_repository.get_by_id.return_value = pokemon
        mock_team_repository.get_trainer_team_size.return_value = 6

        with pytest.raises(BusinessRuleException, match="Maximum 6 Pokemon per team"):
            team_service.add_pokemon_to_team(add_dto)

    def test_add_pokemon_already_in_team(
        self,
        team_service: TeamService,
        mock_trainer_repository: Mock,
        mock_pokemon_repository: Mock,
        mock_team_repository: Mock,
    ) -> None:
        add_dto = TeamAddPokemonDTOFactory.add_pikachu_to_ash()
        trainer = TrainerFactory.ash_ketchum()
        pokemon = PokemonFactory.pikachu()
        existing_team_member = TeamFactory.ash_pikachu_team_member()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_pokemon_repository.get_by_id.return_value = pokemon
        mock_team_repository.get_trainer_team_size.return_value = 1
        mock_team_repository.get_team_member.return_value = existing_team_member

        with pytest.raises(
            BusinessRuleException, match="Pokemon.*is already in trainer.*team"
        ):
            team_service.add_pokemon_to_team(add_dto)

    def test_add_pokemon_position_occupied(
        self,
        team_service: TeamService,
        mock_trainer_repository: Mock,
        mock_pokemon_repository: Mock,
        mock_team_repository: Mock,
    ) -> None:
        add_dto = TeamAddPokemonDTOFactory.add_pikachu_to_ash()
        trainer = TrainerFactory.ash_ketchum()
        pokemon = PokemonFactory.pikachu()
        existing_team_members = [TeamFactory.ash_charizard_team_member()]
        existing_team_members[0].position = 1

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_pokemon_repository.get_by_id.return_value = pokemon
        mock_team_repository.get_trainer_team_size.return_value = 1
        mock_team_repository.get_team_member.return_value = None
        mock_team_repository.get_team_by_trainer.return_value = existing_team_members

        with pytest.raises(
            BusinessRuleException, match="Position.*is already occupied"
        ):
            team_service.add_pokemon_to_team(add_dto)

    def test_remove_pokemon_from_team_success(
        self,
        team_service: TeamService,
        mock_team_repository: Mock,
        mock_trainer_repository: Mock,
    ) -> None:
        team_member = TeamFactory.ash_pikachu_team_member()
        trainer = TrainerFactory.ash_ketchum()

        mock_team_repository.get_team_member.return_value = team_member
        mock_team_repository.remove_pokemon_from_team.return_value = True
        mock_trainer_repository.get_by_id.return_value = trainer
        mock_team_repository.get_team_by_trainer.return_value = []

        result = team_service.remove_pokemon_from_team(1, 1)

        assert result.trainer_id == 1
        assert result.team_size == 0
        mock_team_repository.remove_pokemon_from_team.assert_called_once_with(1, 1)

    def test_remove_pokemon_not_in_team(
        self, team_service: TeamService, mock_team_repository: Mock
    ) -> None:
        mock_team_repository.get_team_member.return_value = None

        with pytest.raises(
            BusinessRuleException, match="Pokemon.*is not in trainer.*team"
        ):
            team_service.remove_pokemon_from_team(1, 999)

    def test_remove_pokemon_operation_failed(
        self,
        team_service: TeamService,
        mock_team_repository: Mock,
    ) -> None:
        team_member = TeamFactory.ash_pikachu_team_member()
        mock_team_repository.get_team_member.return_value = team_member
        mock_team_repository.remove_pokemon_from_team.return_value = False

        with pytest.raises(
            BusinessRuleException, match="Failed to remove Pokemon from team"
        ):
            team_service.remove_pokemon_from_team(1, 1)

    def test_update_pokemon_position_success(
        self,
        team_service: TeamService,
        mock_team_repository: Mock,
        mock_trainer_repository: Mock,
    ) -> None:
        team_member = TeamFactory.ash_pikachu_team_member()
        trainer = TrainerFactory.ash_ketchum()
        update_dto = TeamUpdatePositionDTOFactory.move_to_position_three()

        mock_team_repository.get_team_member.return_value = team_member
        mock_team_repository.get_team_by_trainer.return_value = []
        mock_team_repository.update_position.return_value = None
        mock_trainer_repository.get_by_id.return_value = trainer

        result = team_service.update_pokemon_position(1, 1, update_dto)

        assert result.trainer_id == 1
        mock_team_repository.update_position.assert_called_once_with(1, 1, 3)

    def test_update_pokemon_position_not_in_team(
        self, team_service: TeamService, mock_team_repository: Mock
    ) -> None:
        update_dto = TeamUpdatePositionDTOFactory.move_to_position_three()
        mock_team_repository.get_team_member.return_value = None

        with pytest.raises(
            BusinessRuleException, match="Pokemon.*is not in trainer.*team"
        ):
            team_service.update_pokemon_position(1, 999, update_dto)

    def test_update_pokemon_position_occupied(
        self, team_service: TeamService, mock_team_repository: Mock
    ) -> None:
        team_member = TeamFactory.ash_pikachu_team_member()
        existing_members = [
            TeamFactory.build(trainer_id=1, pokemon_id=2, position=3, is_active=True)
        ]
        update_dto = TeamUpdatePositionDTOFactory.move_to_position_three()

        mock_team_repository.get_team_member.return_value = team_member
        mock_team_repository.get_team_by_trainer.return_value = existing_members

        with pytest.raises(
            BusinessRuleException, match="Position.*is already occupied"
        ):
            team_service.update_pokemon_position(1, 1, update_dto)

    def test_get_trainer_team_success(
        self,
        team_service: TeamService,
        mock_trainer_repository: Mock,
        mock_team_repository: Mock,
        mock_pokemon_repository: Mock,
    ) -> None:
        trainer = TrainerFactory.ash_ketchum()
        team_members = [TeamFactory.ash_pikachu_team_member()]
        pokemon = PokemonFactory.pikachu()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_team_repository.get_team_by_trainer.return_value = team_members
        mock_pokemon_repository.get_by_id.return_value = pokemon

        result = team_service.get_trainer_team(1)

        assert result.trainer_id == 1
        assert result.trainer_name == "Ash Ketchum"
        assert result.team_size == 1
        assert len(result.members) == 1
        assert result.members[0].pokemon_name == "Pikachu"

    def test_get_trainer_team_trainer_not_found(
        self, team_service: TeamService, mock_trainer_repository: Mock
    ) -> None:
        mock_trainer_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Trainer.*999"):
            team_service.get_trainer_team(999)

    def test_get_trainer_team_empty(
        self,
        team_service: TeamService,
        mock_trainer_repository: Mock,
        mock_team_repository: Mock,
    ) -> None:
        trainer = TrainerFactory.ash_ketchum()

        mock_trainer_repository.get_by_id.return_value = trainer
        mock_team_repository.get_team_by_trainer.return_value = []

        result = team_service.get_trainer_team(1)

        assert result.trainer_id == 1
        assert result.team_size == 0
        assert len(result.members) == 0

    def test_team_entity_position_validation_high(self) -> None:
        with pytest.raises(ValueError, match="Position must be between 1 and 6"):
            TeamFactory.invalid_position_high()

    def test_team_entity_position_validation_low(self) -> None:
        with pytest.raises(ValueError, match="Position must be between 1 and 6"):
            TeamFactory.invalid_position_low()

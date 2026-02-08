from unittest.mock import Mock

import pytest

from src.application.services.trainer_service import TrainerService
from src.domain.enums.trainer_enums import Gender, Region
from tests.factories.trainer_factories import (
    PokemonSummaryDTOFactory,
    TrainerCreateDTOFactory,
    TrainerFactory,
    TrainerUpdateDTOFactory,
)


class TestTrainerService:
    @pytest.fixture
    def trainer_service(self, mock_trainer_repository: Mock) -> TrainerService:
        return TrainerService(
            trainer_repository=mock_trainer_repository,
            team_repository=None,
            pokemon_repository=None,
        )

    @pytest.fixture
    def trainer_service_with_deps(
        self,
        mock_trainer_repository: Mock,
        mock_team_repository: Mock,
        mock_pokemon_repository: Mock
    ) -> TrainerService:
        mock_team_repository.get_team_by_trainer.return_value = []
        return TrainerService(
            trainer_repository=mock_trainer_repository,
            team_repository=mock_team_repository,
            pokemon_repository=mock_pokemon_repository,
        )

    def test_create_trainer_success(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        create_dto = TrainerCreateDTOFactory.ash_ketchum()
        trainer = TrainerFactory.ash_ketchum()
        mock_trainer_repository.create.return_value = trainer

        result = trainer_service.create_trainer(create_dto)

        assert result.name == trainer.name
        assert result.gender == trainer.gender.value
        assert result.region == trainer.region.value
        assert result.team_size == 0
        mock_trainer_repository.create.assert_called_once()

    def test_create_trainer_random_data(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        create_dto = TrainerCreateDTOFactory.random_trainer()
        trainer = TrainerFactory.build()
        mock_trainer_repository.create.return_value = trainer

        result = trainer_service.create_trainer(create_dto)

        assert result is not None
        assert result.name == trainer.name
        mock_trainer_repository.create.assert_called_once()

    def test_get_trainer_found(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        trainer = TrainerFactory.ash_ketchum()
        mock_trainer_repository.get_by_id.return_value = trainer

        result = trainer_service.get_trainer(1)

        assert result is not None
        assert result.id == trainer.id
        assert result.name == trainer.name
        assert result.gender == trainer.gender.value
        assert result.region == trainer.region.value
        mock_trainer_repository.get_by_id.assert_called_once_with(1)

    def test_get_trainer_not_found(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        mock_trainer_repository.get_by_id.return_value = None

        result = trainer_service.get_trainer(999)

        assert result is None
        mock_trainer_repository.get_by_id.assert_called_once_with(999)

    def test_get_all_trainers_success(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        trainer_list = TrainerFactory.batch(size=3)
        mock_trainer_repository.get_all.return_value = trainer_list

        result = trainer_service.get_all_trainers(skip=0, limit=10)

        assert len(result) == 3
        for i, trainer_dto in enumerate(result):
            assert trainer_dto.name == trainer_list[i].name
            assert trainer_dto.gender == trainer_list[i].gender.value
        mock_trainer_repository.get_all.assert_called_once_with(0, 10)

    def test_get_all_trainers_empty_list(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        mock_trainer_repository.get_all.return_value = []

        result = trainer_service.get_all_trainers()

        assert len(result) == 0
        mock_trainer_repository.get_all.assert_called_once_with(0, 100)

    def test_get_all_trainers_with_pagination(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        trainer_list = TrainerFactory.batch(size=5)
        mock_trainer_repository.get_all.return_value = trainer_list

        result = trainer_service.get_all_trainers(skip=10, limit=20)

        assert len(result) == 5
        mock_trainer_repository.get_all.assert_called_once_with(10, 20)

    def test_update_trainer_success(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        existing_trainer = TrainerFactory.ash_ketchum()
        updated_trainer = TrainerFactory.build(id=1, name="Updated Ash")
        update_dto = TrainerUpdateDTOFactory.name_only()

        mock_trainer_repository.get_by_id.return_value = existing_trainer
        mock_trainer_repository.update.return_value = updated_trainer

        result = trainer_service.update_trainer(1, update_dto)

        assert result is not None
        assert result.name == updated_trainer.name
        mock_trainer_repository.get_by_id.assert_called_once_with(1)
        mock_trainer_repository.update.assert_called_once()

    def test_update_trainer_gender_only(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        existing_trainer = TrainerFactory.ash_ketchum()
        updated_trainer = TrainerFactory.build(id=1, name="Ash Ketchum", gender=Gender.OTHER)
        update_dto = TrainerUpdateDTOFactory.gender_only()

        mock_trainer_repository.get_by_id.return_value = existing_trainer
        mock_trainer_repository.update.return_value = updated_trainer

        result = trainer_service.update_trainer(1, update_dto)

        assert result is not None
        assert result.gender == Gender.OTHER.value
        mock_trainer_repository.update.assert_called_once()

    def test_update_trainer_full_update(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        existing_trainer = TrainerFactory.ash_ketchum()
        updated_trainer = TrainerFactory.build(
            id=1,
            name="Completely Updated Trainer",
            gender=Gender.FEMALE,
            region=Region.HOENN,
        )
        update_dto = TrainerUpdateDTOFactory.full_update()

        mock_trainer_repository.get_by_id.return_value = existing_trainer
        mock_trainer_repository.update.return_value = updated_trainer

        result = trainer_service.update_trainer(1, update_dto)

        assert result is not None
        assert result.name == "Completely Updated Trainer"
        assert result.gender == Gender.FEMALE.value
        assert result.region == Region.HOENN.value

    def test_update_trainer_not_found(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        update_dto = TrainerUpdateDTOFactory.name_only()
        mock_trainer_repository.get_by_id.return_value = None

        result = trainer_service.update_trainer(999, update_dto)

        assert result is None
        mock_trainer_repository.get_by_id.assert_called_once_with(999)
        mock_trainer_repository.update.assert_not_called()

    def test_delete_trainer_success(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        mock_trainer_repository.delete.return_value = True

        result = trainer_service.delete_trainer(1)

        assert result is True
        mock_trainer_repository.delete.assert_called_once_with(1)

    def test_delete_trainer_failure(
        self, trainer_service: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        mock_trainer_repository.delete.return_value = False

        result = trainer_service.delete_trainer(1)

        assert result is False
        mock_trainer_repository.delete.assert_called_once_with(1)

    def test_trainer_with_pokemon_team_empty(
        self, trainer_service_with_deps: TrainerService, mock_trainer_repository: Mock
    ) -> None:
        trainer = TrainerFactory.ash_ketchum()
        mock_trainer_repository.get_by_id.return_value = trainer

        result = trainer_service_with_deps.get_trainer(1)

        assert result is not None
        assert result.team_size == 0
        assert result.pokemon_team == []

    def test_trainer_with_pokemon_team_populated(
        self,
        mock_trainer_repository: Mock,
        mock_team_repository: Mock,
        mock_pokemon_repository: Mock
    ) -> None:
        from tests.factories.pokemon_factories import PokemonFactory

        trainer = TrainerFactory.ash_ketchum()
        mock_trainer_repository.get_by_id.return_value = trainer

        team_members = [Mock(pokemon_id=1), Mock(pokemon_id=2)]
        mock_team_repository.get_team_by_trainer.return_value = team_members

        pokemon1 = PokemonFactory.pikachu()
        pokemon2 = PokemonFactory.charizard()
        mock_pokemon_repository.get_by_id.side_effect = [pokemon1, pokemon2]

        trainer_service_with_deps = TrainerService(
            trainer_repository=mock_trainer_repository,
            team_repository=mock_team_repository,
            pokemon_repository=mock_pokemon_repository,
        )

        result = trainer_service_with_deps.get_trainer(1)

        assert result is not None
        assert result.team_size == 2
        assert len(result.pokemon_team) == 2
        assert result.pokemon_team[0].name == "Pikachu"
        assert result.pokemon_team[1].name == "Charizard"

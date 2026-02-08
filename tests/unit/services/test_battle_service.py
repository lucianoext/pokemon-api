from unittest.mock import Mock

import pytest

from src.application.services.battle_service import BattleService
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException
from tests.factories.battle_factories import (
    BattleCreateDTOFactory,
    BattleFactory,
)
from tests.factories.trainer_factories import TrainerFactory


class TestBattleService:
    @pytest.fixture
    def battle_service(
        self,
        mock_battle_repository: Mock,
        mock_trainer_repository: Mock,
        mock_team_repository: Mock,
    ) -> BattleService:
        return BattleService(
            battle_repository=mock_battle_repository,
            trainer_repository=mock_trainer_repository,
            team_repository=mock_team_repository,
        )

    def test_create_battle_success(
        self,
        battle_service: BattleService,
        mock_battle_repository: Mock,
        mock_trainer_repository: Mock,
        mock_team_repository: Mock,
    ) -> None:
        create_dto = BattleCreateDTOFactory.ash_vs_gary_ash_wins()
        ash = TrainerFactory.ash_ketchum()
        gary = TrainerFactory.gary_oak()
        battle = BattleFactory.ash_vs_gary_ash_wins()

        mock_trainer_repository.get_by_id.side_effect = [ash, gary, ash]
        mock_team_repository.get_trainer_team_size.side_effect = [3, 4]
        mock_battle_repository.create_battle.return_value = battle

        result = battle_service.create_battle(create_dto)

        assert result.team1_trainer_id == 1
        assert result.team2_trainer_id == 2
        assert result.winner_trainer_id == 1
        assert result.team1_trainer_name == "Ash Ketchum"
        assert result.team2_trainer_name == "Gary Oak"
        assert result.winner_trainer_name == "Ash Ketchum"
        mock_battle_repository.create_battle.assert_called_once()

    def test_create_battle_team1_trainer_not_found(
        self, battle_service: BattleService, mock_trainer_repository: Mock
    ) -> None:
        create_dto = BattleCreateDTOFactory.nonexistent_team1_trainer()
        mock_trainer_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Trainer.*999"):
            battle_service.create_battle(create_dto)

    def test_create_battle_team2_trainer_not_found(
        self,
        battle_service: BattleService,
        mock_trainer_repository: Mock,
    ) -> None:
        create_dto = BattleCreateDTOFactory.nonexistent_team2_trainer()
        ash = TrainerFactory.ash_ketchum()
        mock_trainer_repository.get_by_id.side_effect = [ash, None]

        with pytest.raises(EntityNotFoundException, match="Trainer.*999"):
            battle_service.create_battle(create_dto)

    def test_create_battle_winner_trainer_not_found(
        self,
        battle_service: BattleService,
        mock_trainer_repository: Mock,
    ) -> None:
        create_dto = BattleCreateDTOFactory.nonexistent_winner_trainer()
        ash = TrainerFactory.ash_ketchum()
        gary = TrainerFactory.gary_oak()
        mock_trainer_repository.get_by_id.side_effect = [ash, gary, None]

        with pytest.raises(EntityNotFoundException, match="Trainer.*999"):
            battle_service.create_battle(create_dto)

    def test_create_battle_team1_empty(
        self,
        battle_service: BattleService,
        mock_trainer_repository: Mock,
        mock_team_repository: Mock,
    ) -> None:
        create_dto = BattleCreateDTOFactory.empty_team1()
        ash = TrainerFactory.ash_ketchum()
        gary = TrainerFactory.gary_oak()

        mock_trainer_repository.get_by_id.side_effect = [ash, gary, gary]
        mock_team_repository.get_trainer_team_size.side_effect = [0, 4]

        with pytest.raises(BusinessRuleException, match="Ash Ketchum.*has no Pokemon"):
            battle_service.create_battle(create_dto)

    def test_create_battle_team2_empty(
        self,
        battle_service: BattleService,
        mock_trainer_repository: Mock,
        mock_team_repository: Mock,
    ) -> None:
        create_dto = BattleCreateDTOFactory.empty_team2()
        ash = TrainerFactory.ash_ketchum()
        gary = TrainerFactory.gary_oak()

        mock_trainer_repository.get_by_id.side_effect = [ash, gary, ash]
        mock_team_repository.get_trainer_team_size.side_effect = [3, 0]

        with pytest.raises(BusinessRuleException, match="Gary Oak.*has no Pokemon"):
            battle_service.create_battle(create_dto)

    def test_get_all_battles_success(
        self,
        battle_service: BattleService,
        mock_battle_repository: Mock,
        mock_trainer_repository: Mock,
    ) -> None:
        battles = [
            BattleFactory.ash_vs_gary_ash_wins(),
            BattleFactory.gary_vs_misty_gary_wins(),
        ]
        ash = TrainerFactory.ash_ketchum()
        gary = TrainerFactory.gary_oak()
        misty = TrainerFactory.misty()

        mock_battle_repository.get_all.return_value = battles
        mock_trainer_repository.get_by_id.side_effect = [
            ash, gary, ash,
            gary, misty, gary,
        ]

        result = battle_service.get_all_battles(skip=0, limit=10)

        assert len(result) == 2
        assert result[0].team1_trainer_name == "Ash Ketchum"
        assert result[1].team1_trainer_name == "Gary Oak"
        mock_battle_repository.get_all.assert_called_once_with(skip=0, limit=10)

    def test_get_all_battles_empty(
        self, battle_service: BattleService, mock_battle_repository: Mock
    ) -> None:
        mock_battle_repository.get_all.return_value = []

        result = battle_service.get_all_battles()

        assert len(result) == 0
        mock_battle_repository.get_all.assert_called_once_with(skip=0, limit=100)

    def test_get_trainer_battles_success(
        self,
        battle_service: BattleService,
        mock_battle_repository: Mock,
        mock_trainer_repository: Mock,
    ) -> None:
        trainer_id = 1
        battles = [BattleFactory.ash_vs_gary_ash_wins()]
        ash = TrainerFactory.ash_ketchum()
        gary = TrainerFactory.gary_oak()

        mock_trainer_repository.get_by_id.side_effect = [ash, ash, gary, ash]
        mock_battle_repository.get_battles_by_trainer.return_value = battles

        result = battle_service.get_trainer_battles(trainer_id)

        assert len(result) == 1
        assert result[0].team1_trainer_name == "Ash Ketchum"
        mock_battle_repository.get_battles_by_trainer.assert_called_once_with(trainer_id)

    def test_get_trainer_battles_trainer_not_found(
        self, battle_service: BattleService, mock_trainer_repository: Mock
    ) -> None:
        mock_trainer_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Trainer.*999"):
            battle_service.get_trainer_battles(999)

    def test_get_leaderboard_success(
        self, battle_service: BattleService, mock_battle_repository: Mock
    ) -> None:
        leaderboard_data = [
            {
                "trainer_id": 2,
                "trainer_name": "Gary Oak",
                "wins": 18,
                "losses": 5,
                "total_battles": 23,
                "win_rate": 0.783,
            },
            {
                "trainer_id": 1,
                "trainer_name": "Ash Ketchum",
                "wins": 15,
                "losses": 8,
                "total_battles": 23,
                "win_rate": 0.652,
            },
        ]

        mock_battle_repository.get_leaderboard_data.return_value = leaderboard_data

        result = battle_service.get_leaderboard()

        assert len(result.leaderboard) == 2
        assert result.leaderboard[0].trainer_name == "Gary Oak"
        assert result.leaderboard[0].win_rate == 0.783
        assert result.total_trainers == 2
        assert result.total_battles == 23

    def test_get_leaderboard_empty(
        self, battle_service: BattleService, mock_battle_repository: Mock
    ) -> None:
        mock_battle_repository.get_leaderboard_data.return_value = []

        result = battle_service.get_leaderboard()

        assert len(result.leaderboard) == 0
        assert result.total_trainers == 0
        assert result.total_battles == 0

    def test_delete_battle_success(
        self,
        battle_service: BattleService,
        mock_battle_repository: Mock,
    ) -> None:
        battle = BattleFactory.ash_vs_gary_ash_wins()
        mock_battle_repository.get_by_id.return_value = battle
        mock_battle_repository.delete_battle.return_value = True

        result = battle_service.delete_battle(1)

        assert result is True
        mock_battle_repository.delete_battle.assert_called_once_with(1)

    def test_delete_battle_not_found(
        self, battle_service: BattleService, mock_battle_repository: Mock
    ) -> None:
        mock_battle_repository.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException, match="Battle.*999"):
            battle_service.delete_battle(999)

    def test_battle_entity_same_trainer_validation(self) -> None:
        with pytest.raises(ValueError, match="cannot battle themselves"):
            BattleFactory.same_trainer_battle()

    def test_battle_entity_invalid_winner_validation(self) -> None:
        with pytest.raises(ValueError, match="Winner must be one of the battling trainers"):
            BattleFactory.invalid_winner_battle()

    def test_battle_entity_negative_strength_validation(self) -> None:
        with pytest.raises(ValueError, match="Team strength cannot be negative"):
            BattleFactory.negative_strength_battle()

    def test_battle_entity_negative_margin_validation(self) -> None:
        with pytest.raises(ValueError, match="Victory margin cannot be negative"):
            BattleFactory.negative_margin_battle()

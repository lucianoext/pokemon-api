from datetime import datetime, timedelta
from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from src.application.dtos.battle_dto import (
    BattleCreateDTO,
    BattleResponseDTO,
    LeaderboardEntryDTO,
    LeaderboardResponseDTO,
)
from src.domain.entities.battle import Battle


class BattleFactory(DataclassFactory[Battle]):
    __model__ = Battle

    @classmethod
    def ash_vs_gary_ash_wins(cls) -> Battle:
        return cls.build(
            id=1,
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=85.5,
            team2_strength=78.2,
            victory_margin=7.3,
            battle_date=datetime(2024, 1, 15, 14, 30),
            battle_details="Epic battle at Pewter City Gym",
        )

    @classmethod
    def gary_vs_misty_gary_wins(cls) -> Battle:
        return cls.build(
            id=2,
            team1_trainer_id=2,
            team2_trainer_id=3,
            winner_trainer_id=2,
            team1_strength=90.0,
            team2_strength=75.5,
            victory_margin=14.5,
            battle_date=datetime(2024, 1, 20, 16, 45),
            battle_details="Water vs Normal type battle",
        )

    @classmethod
    def misty_vs_ash_misty_wins(cls) -> Battle:
        return cls.build(
            id=3,
            team1_trainer_id=3,
            team2_trainer_id=1,
            winner_trainer_id=3,
            team1_strength=82.0,
            team2_strength=79.0,
            victory_margin=3.0,
            battle_date=datetime(2024, 1, 25, 10, 15),
            battle_details="Close battle at Cerulean Gym",
        )

    @classmethod
    def recent_battle(cls) -> Battle:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=88.0,
            team2_strength=85.0,
            victory_margin=3.0,
            battle_date=datetime.utcnow() - timedelta(hours=1),
        )

    @classmethod
    def close_battle(cls) -> Battle:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=2,
            team1_strength=89.5,
            team2_strength=90.0,
            victory_margin=0.5,
            battle_details="Very close match!",
        )

    @classmethod
    def high_margin_battle(cls) -> Battle:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=95.0,
            team2_strength=60.0,
            victory_margin=35.0,
            battle_details="Dominant victory",
        )

    @classmethod
    def same_trainer_battle(cls) -> Battle:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=1,
            winner_trainer_id=1,
        )

    @classmethod
    def invalid_winner_battle(cls) -> Battle:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=3,
        )

    @classmethod
    def negative_strength_battle(cls) -> Battle:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=-10.0,
            team2_strength=80.0,
        )

    @classmethod
    def negative_margin_battle(cls) -> Battle:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=80.0,
            team2_strength=75.0,
            victory_margin=-5.0,
        )


class BattleCreateDTOFactory(ModelFactory[BattleCreateDTO]):
    __model__ = BattleCreateDTO

    @classmethod
    def ash_vs_gary_ash_wins(cls) -> BattleCreateDTO:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=85.5,
            team2_strength=78.2,
            victory_margin=7.3,
            battle_details="Epic battle at Pewter City Gym",
        )

    @classmethod
    def gary_vs_misty_gary_wins(cls) -> BattleCreateDTO:
        return cls.build(
            team1_trainer_id=2,
            team2_trainer_id=3,
            winner_trainer_id=2,
            team1_strength=90.0,
            team2_strength=75.5,
            victory_margin=14.5,
            battle_details="Water vs Normal type battle",
        )

    @classmethod
    def simple_battle(cls) -> BattleCreateDTO:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=80.0,
            team2_strength=75.0,
            victory_margin=5.0,
        )

    @classmethod
    def nonexistent_team1_trainer(cls) -> BattleCreateDTO:
        return cls.build(
            team1_trainer_id=999,
            team2_trainer_id=2,
            winner_trainer_id=2,
            team1_strength=80.0,
            team2_strength=85.0,
            victory_margin=5.0,
        )

    @classmethod
    def nonexistent_team2_trainer(cls) -> BattleCreateDTO:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=999,
            winner_trainer_id=1,
            team1_strength=85.0,
            team2_strength=80.0,
            victory_margin=5.0,
        )

    @classmethod
    def nonexistent_winner_trainer(cls) -> BattleCreateDTO:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=999,
            team1_strength=80.0,
            team2_strength=75.0,
            victory_margin=5.0,
        )

    @classmethod
    def empty_team1(cls) -> BattleCreateDTO:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=2,
            team1_strength=0.0,
            team2_strength=80.0,
            victory_margin=80.0,
        )

    @classmethod
    def empty_team2(cls) -> BattleCreateDTO:
        return cls.build(
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=80.0,
            team2_strength=0.0,
            victory_margin=80.0,
        )


class BattleResponseDTOFactory(ModelFactory[BattleResponseDTO]):
    __model__ = BattleResponseDTO

    @classmethod
    def from_battle(cls, battle: Battle, trainer_names: dict[int, str] | None = None) -> BattleResponseDTO:
        names = trainer_names or {}
        return cls.build(
            id=battle.id,
            team1_trainer_id=battle.team1_trainer_id,
            team2_trainer_id=battle.team2_trainer_id,
            winner_trainer_id=battle.winner_trainer_id,
            team1_strength=battle.team1_strength,
            team2_strength=battle.team2_strength,
            victory_margin=battle.victory_margin,
            battle_date=battle.battle_date,
            battle_details=battle.battle_details,
            team1_trainer_name=names.get(battle.team1_trainer_id),
            team2_trainer_name=names.get(battle.team2_trainer_id),
            winner_trainer_name=names.get(battle.winner_trainer_id),
        )

    @classmethod
    def ash_vs_gary_complete(cls) -> BattleResponseDTO:
        return cls.build(
            id=1,
            team1_trainer_id=1,
            team2_trainer_id=2,
            winner_trainer_id=1,
            team1_strength=85.5,
            team2_strength=78.2,
            victory_margin=7.3,
            battle_date=datetime(2024, 1, 15, 14, 30),
            battle_details="Epic battle at Pewter City Gym",
            team1_trainer_name="Ash Ketchum",
            team2_trainer_name="Gary Oak",
            winner_trainer_name="Ash Ketchum",
        )


class LeaderboardEntryDTOFactory(ModelFactory[LeaderboardEntryDTO]):
    __model__ = LeaderboardEntryDTO

    @classmethod
    def ash_stats(cls) -> LeaderboardEntryDTO:
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            wins=15,
            losses=8,
            total_battles=23,
            win_rate=0.652,
        )

    @classmethod
    def gary_stats(cls) -> LeaderboardEntryDTO:
        return cls.build(
            trainer_id=2,
            trainer_name="Gary Oak",
            wins=18,
            losses=5,
            total_battles=23,
            win_rate=0.783,
        )

    @classmethod
    def misty_stats(cls) -> LeaderboardEntryDTO:
        return cls.build(
            trainer_id=3,
            trainer_name="Misty",
            wins=12,
            losses=10,
            total_battles=22,
            win_rate=0.545,
        )

    @classmethod
    def perfect_record(cls) -> LeaderboardEntryDTO:
        return cls.build(
            trainer_id=4,
            trainer_name="Champion Red",
            wins=10,
            losses=0,
            total_battles=10,
            win_rate=1.0,
        )

    @classmethod
    def no_battles(cls) -> LeaderboardEntryDTO:
        return cls.build(
            trainer_id=5,
            trainer_name="Rookie Trainer",
            wins=0,
            losses=0,
            total_battles=0,
            win_rate=0.0,
        )


class LeaderboardResponseDTOFactory(ModelFactory[LeaderboardResponseDTO]):
    __model__ = LeaderboardResponseDTO

    @classmethod
    def full_leaderboard(cls) -> LeaderboardResponseDTO:
        return cls.build(
            leaderboard=[
                LeaderboardEntryDTOFactory.gary_stats(),
                LeaderboardEntryDTOFactory.ash_stats(),
                LeaderboardEntryDTOFactory.misty_stats(),
            ],
            total_trainers=3,
            total_battles=68,
        )

    @classmethod
    def empty_leaderboard(cls) -> LeaderboardResponseDTO:
        return cls.build(
            leaderboard=[],
            total_trainers=0,
            total_battles=0,
        )

    @classmethod
    def single_trainer_leaderboard(cls) -> LeaderboardResponseDTO:
        return cls.build(
            leaderboard=[LeaderboardEntryDTOFactory.perfect_record()],
            total_trainers=1,
            total_battles=10,
        )

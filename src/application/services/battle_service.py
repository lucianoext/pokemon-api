# src/application/services/battle_service.py
from datetime import datetime

from src.application.dtos.battle_dto import (
    BattleCreateDTO,
    BattleResponseDTO,
    LeaderboardEntryDTO,
    LeaderboardResponseDTO,
)
from src.domain.entities.battle import Battle
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException
from src.domain.repositories.battle_repository import BattleRepository
from src.domain.repositories.team_repository import TeamRepository
from src.domain.repositories.trainer_repository import TrainerRepository


class BattleService:
    def __init__(
        self,
        battle_repository: BattleRepository,
        trainer_repository: TrainerRepository,
        team_repository: TeamRepository,
    ):
        self.battle_repository = battle_repository
        self.trainer_repository = trainer_repository
        self.team_repository = team_repository

    def create_battle(self, dto: BattleCreateDTO) -> BattleResponseDTO:
        team1_trainer = self.trainer_repository.get_by_id(dto.team1_trainer_id)
        if not team1_trainer:
            raise EntityNotFoundException("Trainer", dto.team1_trainer_id)

        team2_trainer = self.trainer_repository.get_by_id(dto.team2_trainer_id)
        if not team2_trainer:
            raise EntityNotFoundException("Trainer", dto.team2_trainer_id)

        winner_trainer = self.trainer_repository.get_by_id(dto.winner_trainer_id)
        if not winner_trainer:
            raise EntityNotFoundException("Trainer", dto.winner_trainer_id)

        team1_size = self.team_repository.get_trainer_team_size(dto.team1_trainer_id)
        team2_size = self.team_repository.get_trainer_team_size(dto.team2_trainer_id)

        if team1_size == 0:
            raise BusinessRuleException(
                f"Trainer {team1_trainer.name} has no Pokemon in their team"
            )

        if team2_size == 0:
            raise BusinessRuleException(
                f"Trainer {team2_trainer.name} has no Pokemon in their team"
            )

        battle = Battle(
            id=None,
            team1_trainer_id=dto.team1_trainer_id,
            team2_trainer_id=dto.team2_trainer_id,
            winner_trainer_id=dto.winner_trainer_id,
            team1_strength=dto.team1_strength,
            team2_strength=dto.team2_strength,
            victory_margin=dto.victory_margin,
            battle_date=datetime.utcnow(),
            battle_details=dto.battle_details,
        )

        created_battle = self.battle_repository.create_battle(battle)

        return BattleResponseDTO(
            id=created_battle.id or 0,
            team1_trainer_id=created_battle.team1_trainer_id,
            team2_trainer_id=created_battle.team2_trainer_id,
            winner_trainer_id=created_battle.winner_trainer_id,
            team1_strength=created_battle.team1_strength,
            team2_strength=created_battle.team2_strength,
            victory_margin=created_battle.victory_margin,
            battle_date=created_battle.battle_date,
            battle_details=created_battle.battle_details,
            team1_trainer_name=team1_trainer.name,
            team2_trainer_name=team2_trainer.name,
            winner_trainer_name=winner_trainer.name,
        )

    def get_all_battles(
        self, skip: int = 0, limit: int = 100
    ) -> list[BattleResponseDTO]:
        battles = self.battle_repository.get_all(skip=skip, limit=limit)

        battle_dtos = []
        for battle in battles:
            team1_trainer = self.trainer_repository.get_by_id(battle.team1_trainer_id)
            team2_trainer = self.trainer_repository.get_by_id(battle.team2_trainer_id)
            winner_trainer = self.trainer_repository.get_by_id(battle.winner_trainer_id)

            battle_dto = BattleResponseDTO(
                id=battle.id or 0,
                team1_trainer_id=battle.team1_trainer_id,
                team2_trainer_id=battle.team2_trainer_id,
                winner_trainer_id=battle.winner_trainer_id,
                team1_strength=battle.team1_strength,
                team2_strength=battle.team2_strength,
                victory_margin=battle.victory_margin,
                battle_date=battle.battle_date,
                battle_details=battle.battle_details,
                team1_trainer_name=team1_trainer.name if team1_trainer else None,
                team2_trainer_name=team2_trainer.name if team2_trainer else None,
                winner_trainer_name=winner_trainer.name if winner_trainer else None,
            )
            battle_dtos.append(battle_dto)

        return battle_dtos

    def get_trainer_battles(self, trainer_id: int) -> list[BattleResponseDTO]:
        trainer = self.trainer_repository.get_by_id(trainer_id)
        if not trainer:
            raise EntityNotFoundException("Trainer", trainer_id)

        battles = self.battle_repository.get_battles_by_trainer(trainer_id)

        battle_dtos = []
        for battle in battles:
            team1_trainer = self.trainer_repository.get_by_id(battle.team1_trainer_id)
            team2_trainer = self.trainer_repository.get_by_id(battle.team2_trainer_id)
            winner_trainer = self.trainer_repository.get_by_id(battle.winner_trainer_id)

            battle_dto = BattleResponseDTO(
                id=battle.id or 0,
                team1_trainer_id=battle.team1_trainer_id,
                team2_trainer_id=battle.team2_trainer_id,
                winner_trainer_id=battle.winner_trainer_id,
                team1_strength=battle.team1_strength,
                team2_strength=battle.team2_strength,
                victory_margin=battle.victory_margin,
                battle_date=battle.battle_date,
                battle_details=battle.battle_details,
                team1_trainer_name=team1_trainer.name if team1_trainer else None,
                team2_trainer_name=team2_trainer.name if team2_trainer else None,
                winner_trainer_name=winner_trainer.name if winner_trainer else None,
            )
            battle_dtos.append(battle_dto)

        return battle_dtos

    def get_leaderboard(self) -> LeaderboardResponseDTO:
        leaderboard_data = self.battle_repository.get_leaderboard_data()

        leaderboard_entries = [
            LeaderboardEntryDTO(
                trainer_id=entry["trainer_id"],
                trainer_name=entry["trainer_name"],
                wins=entry["wins"],
                losses=entry["losses"],
                total_battles=entry["total_battles"],
                win_rate=entry["win_rate"],
            )
            for entry in leaderboard_data
        ]

        total_battles = sum(entry.total_battles for entry in leaderboard_entries) // 2

        return LeaderboardResponseDTO(
            leaderboard=leaderboard_entries,
            total_trainers=len(leaderboard_entries),
            total_battles=total_battles,
        )

    def delete_battle(self, battle_id: int) -> bool:
        battle = self.battle_repository.get_by_id(battle_id)
        if not battle:
            raise EntityNotFoundException("Battle", battle_id)

        return bool(self.battle_repository.delete_battle(battle_id))

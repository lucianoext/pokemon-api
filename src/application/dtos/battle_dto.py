from datetime import datetime

from pydantic import BaseModel


class BattleCreateDTO(BaseModel):
    team1_trainer_id: int
    team2_trainer_id: int
    winner_trainer_id: int
    team1_strength: float
    team2_strength: float
    victory_margin: float
    battle_details: str | None = None


class BattleResponseDTO(BaseModel):
    id: int | None
    team1_trainer_id: int
    team2_trainer_id: int
    winner_trainer_id: int
    team1_strength: float
    team2_strength: float
    victory_margin: float
    battle_date: datetime
    battle_details: str | None = None

    team1_trainer_name: str | None = None
    team2_trainer_name: str | None = None
    winner_trainer_name: str | None = None


class LeaderboardEntryDTO(BaseModel):
    trainer_id: int
    trainer_name: str
    wins: int
    losses: int
    total_battles: int
    win_rate: float


class LeaderboardResponseDTO(BaseModel):
    leaderboard: list[LeaderboardEntryDTO]
    total_trainers: int
    total_battles: int

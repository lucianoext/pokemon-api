from dataclasses import dataclass
from datetime import datetime


@dataclass
class Battle:
    id: int | None
    team1_trainer_id: int
    team2_trainer_id: int
    winner_trainer_id: int
    team1_strength: float
    team2_strength: float
    victory_margin: float
    battle_date: datetime
    battle_details: str | None = None

    def __post_init__(self) -> None:
        if self.team1_trainer_id == self.team2_trainer_id:
            raise ValueError("A trainer cannot battle themselves")

        if self.winner_trainer_id not in [self.team1_trainer_id, self.team2_trainer_id]:
            raise ValueError("Winner must be one of the battling trainers")

        if self.team1_strength < 0 or self.team2_strength < 0:
            raise ValueError("Team strength cannot be negative")

        if self.victory_margin < 0:
            raise ValueError("Victory margin cannot be negative")

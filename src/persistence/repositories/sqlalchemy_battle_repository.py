from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from src.domain.entities.battle import Battle
from src.domain.repositories.battle_repository import BattleRepository
from src.persistence.database.models import BattleModel, TrainerModel


class SqlAlchemyBattleRepository(BattleRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_battle(self, battle: Battle) -> Battle:
        db_battle = BattleModel(
            team1_trainer_id=battle.team1_trainer_id,
            team2_trainer_id=battle.team2_trainer_id,
            winner_trainer_id=battle.winner_trainer_id,
            team1_strength=battle.team1_strength,
            team2_strength=battle.team2_strength,
            victory_margin=battle.victory_margin,
            battle_date=battle.battle_date,
            battle_details=battle.battle_details,
        )

        self.db.add(db_battle)
        self.db.commit()
        self.db.refresh(db_battle)

        return self._model_to_entity(db_battle)

    def get_by_id(self, battle_id: int) -> Battle | None:
        db_battle = (
            self.db.query(BattleModel).filter(BattleModel.id == battle_id).first()
        )
        return self._model_to_entity(db_battle) if db_battle else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Battle]:
        db_battles = (
            self.db.query(BattleModel)
            .order_by(BattleModel.__table__.c.battle_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._model_to_entity(battle) for battle in db_battles]

    def get_battles_by_trainer(self, trainer_id: int) -> list[Battle]:
        db_battles = (
            self.db.query(BattleModel)
            .filter(
                or_(
                    BattleModel.team1_trainer_id == trainer_id,
                    BattleModel.team2_trainer_id == trainer_id,
                )
            )
            .order_by(BattleModel.__table__.c.battle_date.desc())
            .all()
        )
        return [self._model_to_entity(battle) for battle in db_battles]

    def get_trainer_wins(self, trainer_id: int) -> int:
        count = (
            self.db.query(BattleModel)
            .filter(BattleModel.winner_trainer_id == trainer_id)
            .count()
        )
        return int(count)

    def get_trainer_losses(self, trainer_id: int) -> int:
        count = (
            self.db.query(BattleModel)
            .filter(
                and_(
                    or_(
                        BattleModel.team1_trainer_id == trainer_id,
                        BattleModel.team2_trainer_id == trainer_id,
                    ),
                    BattleModel.winner_trainer_id != trainer_id,
                )
            )
            .count()
        )
        return int(count)

    def get_leaderboard_data(self) -> list[dict]:
        # Get trainer battle statistics
        subquery_wins = (
            self.db.query(
                BattleModel.__table__.c.winner_trainer_id.label("trainer_id"),
                func.count(BattleModel.__table__.c.id).label("wins"),
            )
            .group_by(BattleModel.__table__.c.winner_trainer_id)
            .subquery()
        )

        subquery_total = (
            self.db.query(
                func.coalesce(
                    BattleModel.__table__.c.team1_trainer_id,
                    BattleModel.__table__.c.team2_trainer_id,
                ).label("trainer_id"),
                func.count(BattleModel.__table__.c.id).label("total_battles"),
            )
            .filter(
                or_(
                    BattleModel.__table__.c.team1_trainer_id.isnot(None),
                    BattleModel.__table__.c.team2_trainer_id.isnot(None),
                )
            )
            .group_by(
                func.coalesce(
                    BattleModel.__table__.c.team1_trainer_id,
                    BattleModel.__table__.c.team2_trainer_id,
                )
            )
            .subquery()
        )

        # Join with trainers and calculate statistics
        results = (
            self.db.query(
                TrainerModel.__table__.c.id,
                TrainerModel.__table__.c.name,
                func.coalesce(subquery_wins.c.wins, 0).label("wins"),
                func.coalesce(subquery_total.c.total_battles, 0).label("total_battles"),
            )
            .outerjoin(
                subquery_wins, TrainerModel.__table__.c.id == subquery_wins.c.trainer_id
            )
            .outerjoin(
                subquery_total,
                TrainerModel.__table__.c.id == subquery_total.c.trainer_id,
            )
            .filter(func.coalesce(subquery_total.c.total_battles, 0) > 0)
            .all()
        )

        leaderboard_data = []
        for result in results:
            wins = int(result.wins)
            total = int(result.total_battles)
            losses = total - wins
            win_rate = (wins / total * 100) if total > 0 else 0

            leaderboard_data.append(
                {
                    "trainer_id": result.id,
                    "trainer_name": result.name,
                    "wins": wins,
                    "losses": losses,
                    "total_battles": total,
                    "win_rate": round(win_rate, 2),
                }
            )

        return sorted(
            leaderboard_data, key=lambda x: (x["wins"], x["win_rate"]), reverse=True
        )

    def delete_battle(self, battle_id: int) -> bool:
        db_battle = (
            self.db.query(BattleModel).filter(BattleModel.id == battle_id).first()
        )
        if not db_battle:
            return False

        self.db.delete(db_battle)
        self.db.commit()
        return True

    def _model_to_entity(self, model: BattleModel) -> Battle:
        return Battle(
            id=model.id,
            team1_trainer_id=model.team1_trainer_id,
            team2_trainer_id=model.team2_trainer_id,
            winner_trainer_id=model.winner_trainer_id,
            team1_strength=model.team1_strength,
            team2_strength=model.team2_strength,
            victory_margin=model.victory_margin,
            battle_date=model.battle_date,
            battle_details=model.battle_details,
        )

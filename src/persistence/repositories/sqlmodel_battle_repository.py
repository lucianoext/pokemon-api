from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from src.domain.entities.battle import Battle
from src.domain.repositories.battle_repository import BattleRepository
from src.persistence.database.models import BattleModel, TrainerModel
from src.persistence.repositories.base_sqlmodel_repository import BaseSqlModelRepository


class SqlModelBattleRepository(
    BaseSqlModelRepository[Battle, BattleModel], BattleRepository
):
    def __init__(self, db: Session):
        super().__init__(
            db=db,
            model_class=BattleModel,
            entity_to_model_mapper=self._entity_to_model,
            model_to_entity_mapper=self._model_to_entity,
        )

    def _entity_to_model(self, battle: Battle) -> BattleModel:
        return BattleModel(
            id=battle.id,
            team1_trainer_id=battle.team1_trainer_id,
            team2_trainer_id=battle.team2_trainer_id,
            winner_trainer_id=battle.winner_trainer_id,
            team1_strength=battle.team1_strength,
            team2_strength=battle.team2_strength,
            victory_margin=battle.victory_margin,
            battle_date=battle.battle_date,
            battle_details=battle.battle_details,
        )

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

    def create_battle(self, battle: Battle) -> Battle:
        return self.create(battle)

    def get_battles_by_trainer(self, trainer_id: int) -> list[Battle]:
        db_battles = (
            self.db.query(BattleModel)
            .filter(
                or_(
                    BattleModel.team1_trainer_id == trainer_id,
                    BattleModel.team2_trainer_id == trainer_id,
                )
            )
            .order_by(BattleModel.__table__.c.battle_date.desc())  # ← Cambio aquí
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
        subquery_wins = (
            self.db.query(
                BattleModel.__table__.c.winner_trainer_id.label(
                    "trainer_id"
                ),  # ← Cambio aquí
                func.count(BattleModel.__table__.c.id).label("wins"),  # ← Cambio aquí
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
                    BattleModel.team1_trainer_id is not None,  # ← Cambio aquí
                    BattleModel.team2_trainer_id is not None,  # ← Cambio aquí
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
        return self.delete(battle_id)

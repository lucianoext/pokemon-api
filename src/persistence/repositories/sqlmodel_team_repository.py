from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.domain.entities.team import Team
from src.domain.repositories.team_repository import TeamRepository
from src.persistence.database.models import TeamModel
from src.persistence.repositories.base_sqlmodel_repository import BaseSqlModelRepository


class SqlModelTeamRepository(BaseSqlModelRepository[Team, TeamModel], TeamRepository):
    """SQLModel-based Team repository with generics."""

    def __init__(self, db: Session):
        super().__init__(
            db=db,
            model_class=TeamModel,
            entity_to_model_mapper=self._entity_to_model,
            model_to_entity_mapper=self._model_to_entity,
        )

    def _entity_to_model(self, team: Team) -> TeamModel:
        """Convert Team entity to SQLModel."""
        return TeamModel(
            id=team.id,
            trainer_id=team.trainer_id,
            pokemon_id=team.pokemon_id,
            position=team.position,
            is_active=team.is_active,
        )

    def _model_to_entity(self, model: TeamModel) -> Team:
        """Convert SQLModel to Team entity."""
        return Team(
            id=model.id,
            trainer_id=model.trainer_id,
            pokemon_id=model.pokemon_id,
            position=model.position,
            is_active=model.is_active,
        )

    # Domain-specific methods (not covered by generics)
    def add_pokemon_to_team(self, team: Team) -> Team:
        """Add Pokemon to team - uses generic create."""
        return self.create(team)

    def remove_pokemon_from_team(self, trainer_id: int, pokemon_id: int) -> bool:
        """Remove Pokemon from team - custom logic."""
        db_team = (
            self.db.query(TeamModel)
            .filter(
                and_(
                    TeamModel.trainer_id == trainer_id,
                    TeamModel.pokemon_id == pokemon_id,
                    TeamModel.is_active,
                )
            )
            .first()
        )

        if not db_team:
            return False

        db_team.is_active = False
        self.db.commit()
        return True

    def get_team_by_trainer(self, trainer_id: int) -> list[Team]:
        """Get team by trainer - custom query."""
        db_teams = (
            self.db.query(TeamModel)
            .filter(and_(TeamModel.trainer_id == trainer_id, TeamModel.is_active))
            .order_by(TeamModel.position)
            .all()
        )
        return [self._model_to_entity(team) for team in db_teams]

    def get_team_member(self, trainer_id: int, pokemon_id: int) -> Team | None:
        """Get specific team member - custom query."""
        db_team = (
            self.db.query(TeamModel)
            .filter(
                and_(
                    TeamModel.trainer_id == trainer_id,
                    TeamModel.pokemon_id == pokemon_id,
                    TeamModel.is_active,
                )
            )
            .first()
        )
        return self._model_to_entity(db_team) if db_team else None

    def update_position(
        self, trainer_id: int, pokemon_id: int, new_position: int
    ) -> Team | None:
        """Update Pokemon position - custom logic."""
        db_team = (
            self.db.query(TeamModel)
            .filter(
                and_(
                    TeamModel.trainer_id == trainer_id,
                    TeamModel.pokemon_id == pokemon_id,
                    TeamModel.is_active,
                )
            )
            .first()
        )

        if not db_team:
            return None

        db_team.position = new_position
        self.db.commit()
        self.db.refresh(db_team)
        return self._model_to_entity(db_team)

    def get_trainer_team_size(self, trainer_id: int) -> int:
        """Get team size - custom query."""
        count = (
            self.db.query(TeamModel)
            .filter(and_(TeamModel.trainer_id == trainer_id, TeamModel.is_active))
            .count()
        )
        return int(count)

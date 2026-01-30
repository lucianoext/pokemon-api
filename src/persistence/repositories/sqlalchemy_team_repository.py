from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.domain.repositories.team_repository import TeamRepository
from src.domain.entities.team import Team
from src.persistence.database.models import TeamModel

class SqlAlchemyTeamRepository(TeamRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_pokemon_to_team(self, team: Team) -> Team:
        db_team = TeamModel(
            trainer_id=team.trainer_id,
            pokemon_id=team.pokemon_id,
            position=team.position,
            is_active=team.is_active
        )
        
        self.db.add(db_team)
        self.db.commit()
        self.db.refresh(db_team)
        
        return self._model_to_entity(db_team)
    
    def remove_pokemon_from_team(self, trainer_id: int, pokemon_id: int) -> bool:
        db_team = self.db.query(TeamModel).filter(
            and_(
                TeamModel.trainer_id == trainer_id,
                TeamModel.pokemon_id == pokemon_id,
                TeamModel.is_active == True
            )
        ).first()
        
        if not db_team:
            return False
        
        db_team.is_active = False
        self.db.commit()
        return True
    
    def get_team_by_trainer(self, trainer_id: int) -> list[Team]:
        db_teams = self.db.query(TeamModel).filter(
            and_(
                TeamModel.trainer_id == trainer_id,
                TeamModel.is_active == True
            )
        ).order_by(TeamModel.position).all()
        
        return [self._model_to_entity(team) for team in db_teams]
    
    def get_team_member(self, trainer_id: int, pokemon_id: int) -> Team | None:
        db_team = self.db.query(TeamModel).filter(
            and_(
                TeamModel.trainer_id == trainer_id,
                TeamModel.pokemon_id == pokemon_id,
                TeamModel.is_active == True
            )
        ).first()
        
        return self._model_to_entity(db_team) if db_team else None
    
    def update_position(self, trainer_id: int, pokemon_id: int, new_position: int) -> Team | None:
        db_team = self.db.query(TeamModel).filter(
            and_(
                TeamModel.trainer_id == trainer_id,
                TeamModel.pokemon_id == pokemon_id,
                TeamModel.is_active == True
            )
        ).first()
        
        if not db_team:
            return None
        
        db_team.position = new_position
        self.db.commit()
        self.db.refresh(db_team)
        
        return self._model_to_entity(db_team)
    
    def get_trainer_team_size(self, trainer_id: int) -> int:
        return self.db.query(TeamModel).filter(
            and_(
                TeamModel.trainer_id == trainer_id,
                TeamModel.is_active == True
            )
        ).count()
    
    def _model_to_entity(self, model: TeamModel) -> Team:
        return Team(
            id=model.id,
            trainer_id=model.trainer_id,
            pokemon_id=model.pokemon_id,
            position=model.position,
            is_active=model.is_active
        )
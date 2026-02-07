from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from persistence.repositories.sqlmodel_battle_repository import (
    SqlModelBattleRepository,
)
from src.application.dtos.battle_dto import (
    BattleCreateDTO,
    BattleResponseDTO,
    LeaderboardResponseDTO,
)
from src.application.services.battle_service import BattleService
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException
from src.persistence.database import get_database
from src.persistence.repositories import (
    SqlModelTeamRepository,
    SqlModelTrainerRepository,
)
from src.presentation.dependencies.auth import get_current_user

router = APIRouter(prefix="/battles", tags=["battles"])


def get_battle_service(db: Session = Depends(get_database)) -> BattleService:
    battle_repository = SqlModelBattleRepository(db)
    trainer_repository = SqlModelTrainerRepository(db)
    team_repository = SqlModelTeamRepository(db)
    return BattleService(battle_repository, trainer_repository, team_repository)


@router.post("/", response_model=BattleResponseDTO, status_code=HTTPStatus.CREATED)
def create_battle(
    battle_data: BattleCreateDTO,
    service: BattleService = Depends(get_battle_service),
    current_user: Any = Depends(get_current_user),
) -> BattleResponseDTO:
    """Create a new battle record."""
    try:
        return service.create_battle(battle_data)
    except (BusinessRuleException, EntityNotFoundException) as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e)) from e


@router.get("/", response_model=list[BattleResponseDTO])
def get_all_battles(
    skip: int = 0,
    limit: int = 100,
    service: BattleService = Depends(get_battle_service),
    current_user: Any = Depends(get_current_user),
) -> list[BattleResponseDTO]:
    """Get all battles."""
    try:
        return service.get_all_battles(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e)) from e


@router.get("/trainer/{trainer_id}", response_model=list[BattleResponseDTO])
def get_trainer_battles(
    trainer_id: int,
    service: BattleService = Depends(get_battle_service),
    current_user: Any = Depends(get_current_user),
) -> list[BattleResponseDTO]:
    """Get battles for a specific trainer."""
    try:
        return service.get_trainer_battles(trainer_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e)) from e


@router.get("/leaderboard", response_model=LeaderboardResponseDTO)
def get_leaderboard(
    service: BattleService = Depends(get_battle_service),
    current_user: Any = Depends(get_current_user),
) -> LeaderboardResponseDTO:
    """Get battle leaderboard."""
    try:
        return service.get_leaderboard()
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e)) from e


@router.delete("/{battle_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_battle(
    battle_id: int,
    service: BattleService = Depends(get_battle_service),
    current_user: Any = Depends(get_current_user),
) -> None:
    """Delete a battle record."""
    try:
        success = service.delete_battle(battle_id)
        if not success:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f"Battle {battle_id} not found"
            )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e)) from e

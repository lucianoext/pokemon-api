from typing import List
from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session

from src.persistence.database import get_database
from src.persistence.repositories.sqlalchemy_team_repository import SqlAlchemyTeamRepository
from src.persistence.repositories.sqlalchemy_trainer_repository import SqlAlchemyTrainerRepository
from src.persistence.repositories.sqlalchemy_pokemon_repository import SqlAlchemyPokemonRepository
from src.application.services.team_service import TeamService
from src.application.dtos.team_dto import (
    TeamAddPokemonDTO,
    TeamUpdatePositionDTO,
    TeamResponseDTO
)
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException

router = APIRouter(prefix="/teams", tags=["teams"])

def get_team_service(db: Session = Depends(get_database)) -> TeamService:
    team_repository = SqlAlchemyTeamRepository(db)
    trainer_repository = SqlAlchemyTrainerRepository(db)
    pokemon_repository = SqlAlchemyPokemonRepository(db)
    return TeamService(team_repository, trainer_repository, pokemon_repository)

@router.post("/add-pokemon", response_model=TeamResponseDTO, status_code=HTTPStatus.CREATED)
def add_pokemon_to_team(
    team_data: TeamAddPokemonDTO,
    service: TeamService = Depends(get_team_service)
):
    try:
        return service.add_pokemon_to_team(team_data)
    except (BusinessRuleException, EntityNotFoundException) as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/trainers/{trainer_id}/pokemon/{pokemon_id}", response_model=TeamResponseDTO)
def remove_pokemon_from_team(
    trainer_id: int,
    pokemon_id: int,
    service: TeamService = Depends(get_team_service)
):
    try:
        return service.remove_pokemon_from_team(trainer_id, pokemon_id)
    except (BusinessRuleException, EntityNotFoundException) as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )

@router.put("/trainers/{trainer_id}/pokemon/{pokemon_id}/position", response_model=TeamResponseDTO)
def update_pokemon_position(
    trainer_id: int,
    pokemon_id: int,
    position_data: TeamUpdatePositionDTO,
    service: TeamService = Depends(get_team_service)
):
    try:
        return service.update_pokemon_position(trainer_id, pokemon_id, position_data)
    except (BusinessRuleException, EntityNotFoundException) as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )

@router.get("/trainers/{trainer_id}", response_model=TeamResponseDTO)
def get_trainer_team(
    trainer_id: int,
    service: TeamService = Depends(get_team_service)
):
    try:
        return service.get_trainer_team(trainer_id)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e)
        )
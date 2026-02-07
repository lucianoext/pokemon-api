from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.application.dtos.trainer_dto import (
    TrainerCreateDTO,
    TrainerResponseDTO,
    TrainerUpdateDTO,
)
from src.application.services.trainer_service import TrainerService
from src.persistence.database import get_database
from src.persistence.database.models import UserModel
from src.persistence.repositories import SqlModelTrainerRepository
from src.presentation.dependencies.auth import (
    get_current_active_user,
    get_current_user_optional,
)

router = APIRouter(prefix="/trainers", tags=["trainers"])


def get_trainer_service(db: Session = Depends(get_database)) -> TrainerService:
    trainer_repository = SqlModelTrainerRepository(db)
    return TrainerService(trainer_repository)


@router.post("/", response_model=TrainerResponseDTO, status_code=HTTPStatus.CREATED)
def create_trainer(
    trainer: TrainerCreateDTO,
    service: TrainerService = Depends(get_trainer_service),
    current_user: UserModel = Depends(get_current_active_user),
) -> TrainerResponseDTO:
    return service.create_trainer(trainer)


@router.get("/{trainer_id}", response_model=TrainerResponseDTO)
def get_trainer(
    trainer_id: int,
    service: TrainerService = Depends(get_trainer_service),
    current_user: UserModel | None = Depends(get_current_user_optional),
) -> TrainerResponseDTO:
    trainer = service.get_trainer(trainer_id)
    if not trainer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Trainer with id {trainer_id} not found",
        )
    return trainer


@router.get("/", response_model=list[TrainerResponseDTO])
def get_trainers(
    skip: int = 0,
    limit: int = 100,
    service: TrainerService = Depends(get_trainer_service),
    current_user: UserModel | None = Depends(get_current_user_optional),
) -> list[TrainerResponseDTO]:
    return service.get_all_trainers(skip, limit)


@router.get("/me/trainer", response_model=TrainerResponseDTO)
def get_my_trainer(
    service: TrainerService = Depends(get_trainer_service),
    current_user: UserModel = Depends(get_current_active_user),
) -> TrainerResponseDTO:
    if not current_user.trainer_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="No trainer associated with this user",
        )

    trainer = service.get_trainer(current_user.trainer_id)
    if not trainer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Trainer not found"
        )
    return trainer


@router.put("/{trainer_id}", response_model=TrainerResponseDTO)
def update_trainer(
    trainer_id: int,
    trainer: TrainerUpdateDTO,
    service: TrainerService = Depends(get_trainer_service),
    current_user: UserModel = Depends(get_current_active_user),
) -> TrainerResponseDTO:
    if current_user.trainer_id != trainer_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You can only update your own trainer",
        )

    updated_trainer = service.update_trainer(trainer_id, trainer)
    if not updated_trainer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Trainer with id {trainer_id} not found",
        )
    return updated_trainer


@router.delete("/{trainer_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_trainer(
    trainer_id: int,
    service: TrainerService = Depends(get_trainer_service),
    current_user: UserModel = Depends(get_current_active_user),
) -> None:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Only superusers can delete trainers",
        )

    success = service.delete_trainer(trainer_id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Trainer with id {trainer_id} not found",
        )

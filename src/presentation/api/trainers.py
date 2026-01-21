from typing import List
from fastapi import APIRouter, Depends, HTTPException  # Quitar HTTPStatus de aquí
from http import HTTPStatus  # Importar desde http
from sqlalchemy.orm import Session

# Imports
from src.infrastructure.database import get_database
from src.infrastructure.repositories.sqlalchemy_trainer_repository import SqlAlchemyTrainerRepository
from src.application.services.trainer_service import TrainerService
from src.application.dtos.trainer_dto import (
    TrainerCreateDTO, 
    TrainerResponseDTO, 
    TrainerUpdateDTO
)

router = APIRouter(prefix="/trainers", tags=["trainers"])

def get_trainer_service(db: Session = Depends(get_database)) -> TrainerService:
    """Dependency injection para TrainerService"""
    trainer_repository = SqlAlchemyTrainerRepository(db)
    return TrainerService(trainer_repository)

@router.post("/", response_model=TrainerResponseDTO, status_code=HTTPStatus.CREATED)
def create_trainer(
    trainer: TrainerCreateDTO,
    service: TrainerService = Depends(get_trainer_service)
):
    """
    Crear un nuevo entrenador Pokemon
    
    - **name**: Nombre del entrenador
    - **gender**: Género del entrenador (male, female, other)  
    - **region**: Región de origen (kanto, johto, hoenn, etc.)
    """
    return service.create_trainer(trainer)

@router.get("/{trainer_id}", response_model=TrainerResponseDTO)
def get_trainer(
    trainer_id: int,
    service: TrainerService = Depends(get_trainer_service)
):
    """Obtener un entrenador por ID"""
    trainer = service.get_trainer(trainer_id)
    if not trainer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Trainer with id {trainer_id} not found"
        )
    return trainer

@router.get("/", response_model=List[TrainerResponseDTO])
def get_trainers(
    skip: int = 0,
    limit: int = 100,
    service: TrainerService = Depends(get_trainer_service)
):
    """Obtener lista de entrenadores"""
    return service.get_all_trainers(skip, limit)

@router.put("/{trainer_id}", response_model=TrainerResponseDTO)
def update_trainer(
    trainer_id: int,
    trainer: TrainerUpdateDTO,
    service: TrainerService = Depends(get_trainer_service)
):
    """Actualizar un entrenador"""
    updated_trainer = service.update_trainer(trainer_id, trainer)
    if not updated_trainer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Trainer with id {trainer_id} not found"
        )
    return updated_trainer

@router.delete("/{trainer_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_trainer(
    trainer_id: int,
    service: TrainerService = Depends(get_trainer_service)
):
    """Eliminar un entrenador"""
    success = service.delete_trainer(trainer_id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Trainer with id {trainer_id} not found"
        )
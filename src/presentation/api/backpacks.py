from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.application.dtos.backpack_dto import (
    BackpackAddItemDTO,
    BackpackRemoveItemDTO,
    BackpackResponseDTO,
    BackpackUpdateQuantityDTO,
)
from src.application.services.backpack_service import BackpackService
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException
from src.persistence.database import get_database
from src.persistence.repositories import (
    SqlModelBackpackRepository,
    SqlModelItemRepository,
    SqlModelTrainerRepository,
)

router = APIRouter(prefix="/backpacks", tags=["backpacks"])


def get_backpack_service(db: Session = Depends(get_database)) -> BackpackService:
    backpack_repository = SqlModelBackpackRepository(db)
    trainer_repository = SqlModelTrainerRepository(db)
    item_repository = SqlModelItemRepository(db)
    return BackpackService(backpack_repository, trainer_repository, item_repository)


@router.post(
    "/add-item", response_model=BackpackResponseDTO, status_code=HTTPStatus.CREATED
)
def add_item_to_backpack(
    backpack_data: BackpackAddItemDTO,
    service: BackpackService = Depends(get_backpack_service),
) -> BackpackResponseDTO:
    try:
        return service.add_item_to_backpack(backpack_data)
    except (BusinessRuleException, EntityNotFoundException) as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.delete(
    "/trainers/{trainer_id}/items/{item_id}", response_model=BackpackResponseDTO
)
def remove_item_from_backpack(
    trainer_id: int,
    item_id: int,
    remove_data: BackpackRemoveItemDTO,
    service: BackpackService = Depends(get_backpack_service),
) -> BackpackResponseDTO:
    try:
        return service.remove_item_from_backpack(trainer_id, item_id, remove_data)
    except (BusinessRuleException, EntityNotFoundException) as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.put(
    "/trainers/{trainer_id}/items/{item_id}/quantity",
    response_model=BackpackResponseDTO,
)
def update_item_quantity(
    trainer_id: int,
    item_id: int,
    quantity_data: BackpackUpdateQuantityDTO,
    service: BackpackService = Depends(get_backpack_service),
) -> BackpackResponseDTO:
    try:
        return service.update_item_quantity(trainer_id, item_id, quantity_data)
    except (BusinessRuleException, EntityNotFoundException) as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.get("/trainers/{trainer_id}", response_model=BackpackResponseDTO)
def get_trainer_backpack(
    trainer_id: int, service: BackpackService = Depends(get_backpack_service)
) -> BackpackResponseDTO:
    try:
        return service.get_trainer_backpack(trainer_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete("/trainers/{trainer_id}/clear", response_model=BackpackResponseDTO)
def clear_backpack(
    trainer_id: int, service: BackpackService = Depends(get_backpack_service)
) -> BackpackResponseDTO:
    try:
        return service.clear_backpack(trainer_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

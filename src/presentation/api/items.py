from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session

from src.persistence.database import get_database
from src.persistence.repositories.sqlalchemy_item_repository import SqlAlchemyItemRepository
from src.application.services.item_service import ItemService
from src.application.dtos.item_dto import (
    ItemCreateDTO,
    ItemUpdateDTO,
    ItemResponseDTO
)

router = APIRouter(prefix="/items", tags=["items"])

def get_item_service(db: Session = Depends(get_database)) -> ItemService:
    item_repository = SqlAlchemyItemRepository(db)
    return ItemService(item_repository)

@router.post("/", response_model=ItemResponseDTO, status_code=HTTPStatus.CREATED)
def create_item(
    item: ItemCreateDTO,
    service: ItemService = Depends(get_item_service)
):
    return service.create_item(item)

@router.get("/{item_id}", response_model=ItemResponseDTO)
def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item

@router.get("/", response_model=list[ItemResponseDTO])
def get_items(
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service)
):
    return service.get_all_items(skip, limit)

@router.put("/{item_id}", response_model=ItemResponseDTO)
def update_item(
    item_id: int,
    item: ItemUpdateDTO,
    service: ItemService = Depends(get_item_service)
):
    updated_item = service.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return updated_item

@router.delete("/{item_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    success = service.delete_item(item_id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

@router.get("/type/{item_type}", response_model=list[ItemResponseDTO])
def get_items_by_type(
    item_type: str,
    service: ItemService = Depends(get_item_service)
):
    return service.get_items_by_type(item_type)
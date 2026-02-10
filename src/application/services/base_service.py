from typing import TypeVar

from pydantic import BaseModel

from src.domain.protocols.entity_protocol import (
    CreateDTOProtocol,
    EntityProtocol,
    ResponseDTOProtocol,
    UpdateDTOProtocol,
)
from src.domain.repositories.base_repository import BaseRepository

EntityType = TypeVar("EntityType", bound=EntityProtocol)
CreateDTOType = TypeVar("CreateDTOType", bound=CreateDTOProtocol)
UpdateDTOType = TypeVar("UpdateDTOType", bound=UpdateDTOProtocol)
ResponseDTOType = TypeVar("ResponseDTOType", bound=ResponseDTOProtocol)


class BaseService[
    EntityType: EntityProtocol,
    CreateDTOType: CreateDTOProtocol,
    UpdateDTOType: UpdateDTOProtocol,
    ResponseDTOType: ResponseDTOProtocol,
]:
    def __init__(self, repository: BaseRepository[EntityType]):
        self.repository = repository

    def create(self, dto: CreateDTOType) -> ResponseDTOType:
        self._validate_business_rules_for_creation(dto)
        entity = self._dto_to_entity(dto)
        created_entity = self.repository.create(entity)
        return self._transform_to_response_dto(created_entity)

    def get_by_id(self, entity_id: int) -> ResponseDTOType | None:
        entity = self.repository.get_by_id(entity_id)
        return self._transform_to_response_dto(entity) if entity else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ResponseDTOType]:
        entities = self.repository.get_all(skip, limit)
        return [self._transform_to_response_dto(entity) for entity in entities]

    def update(self, entity_id: int, dto: UpdateDTOType) -> ResponseDTOType | None:
        existing_entity = self.repository.get_by_id(entity_id)
        if not existing_entity:
            return None

        updated_entity = self._apply_update_dto(existing_entity, dto)
        self._validate_business_rules_for_update(updated_entity)

        saved_entity = self.repository.update(entity_id, updated_entity)
        return self._transform_to_response_dto(saved_entity) if saved_entity else None

    def delete(self, entity_id: int) -> bool:
        return self.repository.delete(entity_id)

    def _validate_business_rules_for_creation(self, dto: CreateDTOType) -> None:
        pass

    def _validate_business_rules_for_update(self, entity: EntityType) -> None:
        pass

    def _dto_to_entity(self, dto: CreateDTOType) -> EntityType:
        raise NotImplementedError("Subclasses must implement _dto_to_entity")

    def _transform_to_response_dto(self, entity: EntityType) -> ResponseDTOType:
        raise NotImplementedError(
            "Subclasses must implement _transform_to_response_dto"
        )

    def _apply_update_dto(
        self, existing_entity: EntityType, dto: UpdateDTOType
    ) -> EntityType:
        raise NotImplementedError("Subclasses must implement _apply_update_dto")

    def _get_dto_non_none_fields(self, dto: BaseModel) -> dict:
        return {k: v for k, v in dto.model_dump().items() if v is not None}

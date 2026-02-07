from abc import ABC, abstractmethod
from typing import TypeVar

from src.domain.protocols.entity_protocol import EntityProtocol

EntityType = TypeVar("EntityType", bound=EntityProtocol)


class BaseRepository[EntityType: EntityProtocol](ABC):
    """Generic base repository with common CRUD operations."""

    @abstractmethod
    def create(self, entity: EntityType) -> EntityType:
        """Create a new entity."""

    @abstractmethod
    def get_by_id(self, entity_id: int) -> EntityType | None:
        """Get entity by ID."""

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[EntityType]:
        """Get all entities with pagination."""

    @abstractmethod
    def update(self, entity_id: int, entity: EntityType) -> EntityType | None:
        """Update an existing entity."""

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity by ID."""

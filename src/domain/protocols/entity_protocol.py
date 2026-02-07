from typing import Protocol, runtime_checkable


@runtime_checkable
class EntityProtocol(Protocol):
    """Protocol for domain entities with ID field."""

    id: int | None


@runtime_checkable
class CreateDTOProtocol(Protocol):
    """Protocol for creation DTOs."""

    pass


@runtime_checkable
class UpdateDTOProtocol(Protocol):
    """Protocol for update DTOs with optional fields."""

    pass


@runtime_checkable
class ResponseDTOProtocol(Protocol):
    """Protocol for response DTOs."""

    id: int | None

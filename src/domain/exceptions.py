from typing import Any


class PokemonDomainException(Exception):
    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[Any, Any] | None = None,
    ):
        self.message = message
        self.error_code = error_code or "DOMAIN_ERROR"
        self.details = details or {}
        super().__init__(message)


class BusinessRuleException(PokemonDomainException):
    def __init__(self, message: str, rule_name: str | None = None):
        self.rule_name = rule_name
        error_code = (
            f"BUSINESS_RULE_{rule_name}" if rule_name else "BUSINESS_RULE_VIOLATION"
        )
        super().__init__(message, error_code)


class ValidationException(PokemonDomainException):
    def __init__(self, message: str, field_name: str | None = None):
        self.field_name = field_name
        error_code = f"VALIDATION_{field_name}" if field_name else "VALIDATION_ERROR"
        super().__init__(message, error_code)


class EntityNotFoundException(PokemonDomainException):
    def __init__(self, entity_type: str, entity_id: Any):
        self.entity_type = entity_type
        self.entity_id = entity_id
        message = f"{entity_type} with id '{entity_id}' not found"
        super().__init__(message, "ENTITY_NOT_FOUND")

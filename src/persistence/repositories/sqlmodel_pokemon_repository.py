# src/persistence/repositories/sqlmodel_pokemon_repository.py
import json
from typing import Any

from sqlalchemy.orm import Session

from src.domain.entities.pokemon import Pokemon, PokemonNature, PokemonType
from src.domain.repositories.pokemon_repository import PokemonRepository
from src.persistence.database.models import PokemonModel
from src.persistence.repositories.base_sqlmodel_repository import BaseSqlModelRepository


class SqlModelPokemonRepository(
    BaseSqlModelRepository[Pokemon, PokemonModel], PokemonRepository
):
    """SQLModel-based Pokemon repository with generics."""

    def __init__(self, db: Session):
        super().__init__(
            db=db,
            model_class=PokemonModel,
            entity_to_model_mapper=self._entity_to_model,
            model_to_entity_mapper=self._model_to_entity,
        )

    def _entity_to_model(self, pokemon: Pokemon) -> PokemonModel:
        """Convert Pokemon entity to SQLModel."""
        return PokemonModel(
            id=pokemon.id,
            name=pokemon.name,
            type_primary=self._get_enum_value(pokemon.type_primary),
            type_secondary=self._get_enum_value(pokemon.type_secondary)
            if pokemon.type_secondary
            else None,
            attacks=json.dumps(pokemon.attacks) if pokemon.attacks else "[]",
            nature=self._get_enum_value(pokemon.nature),
            level=pokemon.level,
        )

    def _model_to_entity(self, model: PokemonModel) -> Pokemon:
        """Convert SQLModel to Pokemon entity."""
        attacks_list = []
        if model.attacks:
            try:
                attacks_list = json.loads(model.attacks)
            except json.JSONDecodeError:
                attacks_list = []

        return Pokemon(
            id=model.id,
            name=model.name,
            type_primary=PokemonType(model.type_primary),
            type_secondary=PokemonType(model.type_secondary)
            if model.type_secondary
            else None,
            attacks=attacks_list,
            nature=PokemonNature(model.nature),
            level=model.level,
        )

    def _get_enum_value(self, field: Any) -> str | None:
        """Get string value from enum."""
        if field is None:
            return None
        return field.value if hasattr(field, "value") else str(field)

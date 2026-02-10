from src.application.dtos.pokemon_dto import (
    PokemonCreateDTO,
    PokemonResponseDTO,
    PokemonUpdateDTO,
)
from src.application.services.base_service import BaseService
from src.domain import BusinessRuleException
from src.domain.entities.pokemon import Pokemon
from src.domain.repositories.pokemon_repository import PokemonRepository


class PokemonService(
    BaseService[Pokemon, PokemonCreateDTO, PokemonUpdateDTO, PokemonResponseDTO]
):
    def __init__(self, pokemon_repository: PokemonRepository):
        super().__init__(pokemon_repository)

    def create_pokemon(self, dto: PokemonCreateDTO) -> PokemonResponseDTO:
        return self.create(dto)

    def get_pokemon(self, pokemon_id: int) -> PokemonResponseDTO | None:
        return self.get_by_id(pokemon_id)

    def get_all_pokemon(
        self, skip: int = 0, limit: int = 100
    ) -> list[PokemonResponseDTO]:
        return self.get_all(skip, limit)

    def update_pokemon(
        self, pokemon_id: int, pokemon_dto: PokemonUpdateDTO
    ) -> PokemonResponseDTO | None:
        return self.update(pokemon_id, pokemon_dto)

    def delete_pokemon(self, pokemon_id: int) -> bool:
        return self.delete(pokemon_id)

    def level_up_pokemon(
        self, pokemon_id: int, levels: int = 1
    ) -> PokemonResponseDTO | None:
        pokemon = self.repository.get_by_id(pokemon_id)
        if not pokemon:
            return None

        if pokemon.level + levels > 100:
            raise BusinessRuleException("The level cap is 100")

        pokemon.level += levels
        updated_pokemon = self.repository.update(pokemon_id, pokemon)
        return (
            self._transform_to_response_dto(updated_pokemon)
            if updated_pokemon
            else None
        )

    def learn_new_attack(
        self, pokemon_id: int, new_attack: str, replace_attack: str | None = None
    ) -> PokemonResponseDTO | None:
        pokemon = self.repository.get_by_id(pokemon_id)
        if not pokemon:
            return None

        attacks_list = pokemon.attacks.copy()

        if new_attack in attacks_list:
            raise BusinessRuleException(
                f"'{pokemon.name}' already knows '{new_attack}'"
            )

        if len(attacks_list) >= 4:
            if not replace_attack:
                raise BusinessRuleException(
                    f"'{pokemon.name}' already knows 4 attacks. You must specify which one to replace."
                )

            if replace_attack not in attacks_list:
                raise BusinessRuleException(
                    f"'{pokemon.name}' doesn't know '{replace_attack}'"
                )

            attacks_list.remove(replace_attack)

        attacks_list.append(new_attack)
        pokemon.attacks = attacks_list

        updated_pokemon = self.repository.update(pokemon_id, pokemon)
        return (
            self._transform_to_response_dto(updated_pokemon)
            if updated_pokemon
            else None
        )

    def _validate_business_rules_for_creation(self, dto: PokemonCreateDTO) -> None:
        if dto.level < 1 or dto.level > 100:
            raise BusinessRuleException(
                f"Pokemon level must be between 1 and 100, got: {dto.level}"
            )

        if dto.level > 30 and len(dto.attacks) < 3:
            raise BusinessRuleException(
                "Pokemon above level 30 should know at least 3 attacks"
            )

        self._validate_powerful_attacks(dto.attacks, dto.level)

    def _validate_business_rules_for_update(self, pokemon: Pokemon) -> None:
        if pokemon.level < 1 or pokemon.level > 100:
            raise BusinessRuleException(
                f"Pokemon level must be between 1 and 100, got: {pokemon.level}"
            )

        if pokemon.level > 30 and len(pokemon.attacks) < 3:
            raise BusinessRuleException(
                "Pokemon above level 30 should know at least 3 attacks"
            )

        self._validate_powerful_attacks(pokemon.attacks, pokemon.level)

    def _dto_to_entity(self, dto: PokemonCreateDTO) -> Pokemon:
        return Pokemon(
            id=None,
            name=dto.name,
            type_primary=dto.type_primary,
            type_secondary=dto.type_secondary,
            attacks=dto.attacks,
            nature=dto.nature,
            level=dto.level,
        )

    def _transform_to_response_dto(self, pokemon: Pokemon) -> PokemonResponseDTO:
        return PokemonResponseDTO(
            id=pokemon.id,
            name=pokemon.name,
            type_primary=pokemon.type_primary.value,
            type_secondary=pokemon.type_secondary.value
            if pokemon.type_secondary
            else None,
            attacks=pokemon.attacks,
            nature=pokemon.nature.value,
            level=pokemon.level,
        )

    def _apply_update_dto(
        self, existing_pokemon: Pokemon, dto: PokemonUpdateDTO
    ) -> Pokemon:
        non_none_fields = self._get_dto_non_none_fields(dto)

        return Pokemon(
            id=existing_pokemon.id,
            name=non_none_fields.get("name", existing_pokemon.name),
            type_primary=non_none_fields.get(
                "type_primary", existing_pokemon.type_primary
            ),
            type_secondary=non_none_fields.get(
                "type_secondary", existing_pokemon.type_secondary
            ),
            attacks=non_none_fields.get("attacks", existing_pokemon.attacks),
            nature=non_none_fields.get("nature", existing_pokemon.nature),
            level=non_none_fields.get("level", existing_pokemon.level),
        )

    def _validate_powerful_attacks(self, attacks_list: list[str], level: int) -> None:
        powerful_attacks = {
            "Hyper Beam": 50,
            "Solar Beam": 40,
            "Thunder": 25,
            "Blizzard": 35,
        }

        for attack in attacks_list:
            if attack in powerful_attacks:
                required_level = powerful_attacks[attack]
                if level < required_level:
                    raise BusinessRuleException(
                        f"Attack '{attack}' requires level {required_level}"
                    )

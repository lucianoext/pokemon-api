from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from src.application.dtos.pokemon_dto import (
    PokemonCreateDTO,
    PokemonResponseDTO,
    PokemonUpdateDTO,
)
from src.domain.entities.pokemon import Pokemon
from src.domain.enums.pokemon_enums import PokemonNature, PokemonType


class PokemonFactory(DataclassFactory[Pokemon]):
    __model__ = Pokemon

    @classmethod
    def pikachu(cls) -> Pokemon:
        return cls.build(
            id=1,
            name="Pikachu",
            type_primary=PokemonType.ELECTRIC,
            type_secondary=None,
            attacks=["Thunder Shock", "Quick Attack"],
            nature=PokemonNature.JOLLY,
            level=25,
        )

    @classmethod
    def charizard(cls) -> Pokemon:
        return cls.build(
            id=2,
            name="Charizard",
            type_primary=PokemonType.FIRE,
            type_secondary=PokemonType.FLYING,
            attacks=["Flamethrower", "Dragon Claw", "Air Slash"],
            nature=PokemonNature.ADAMANT,
            level=36,
        )

    @classmethod
    def high_level(cls) -> Pokemon:
        return cls.build(level=cls.__faker__.random_int(min=50, max=100))

    @classmethod
    def low_level(cls) -> Pokemon:
        return cls.build(level=cls.__faker__.random_int(min=1, max=10))

    @classmethod
    def max_level(cls) -> Pokemon:
        return cls.build(level=100)

    @classmethod
    def with_four_attacks(cls) -> Pokemon:
        return cls.build(
            attacks=["Move 1", "Move 2", "Move 3", "Move 4"],
            level=cls.__faker__.random_int(min=40, max=100),
        )


class PokemonCreateDTOFactory(ModelFactory[PokemonCreateDTO]):
    __model__ = PokemonCreateDTO

    @classmethod
    def charizard(cls) -> PokemonCreateDTO:
        return cls.build(
            name="Charizard",
            type_primary=PokemonType.FIRE,
            type_secondary=PokemonType.FLYING,
            attacks=["Flamethrower", "Dragon Claw", "Air Slash"],
            nature=PokemonNature.ADAMANT,
            level=36,
        )

    @classmethod
    def invalid_level_high(cls) -> PokemonCreateDTO:
        return cls.build(level=150)

    @classmethod
    def invalid_level_low(cls) -> PokemonCreateDTO:
        return cls.build(level=0)

    @classmethod
    def with_powerful_attack_low_level(cls) -> PokemonCreateDTO:
        return cls.build(
            level=5,
            attacks=["Tackle", "Hyper Beam"],
        )

    @classmethod
    def high_level_few_attacks(cls) -> PokemonCreateDTO:
        return cls.build(
            level=50,
            attacks=["Tackle", "Quick Attack"],
        )

    @classmethod
    def valid_low_level(cls) -> PokemonCreateDTO:
        return cls.build(
            level=cls.__faker__.random_int(min=1, max=30),
            attacks=["Tackle", "Quick Attack"],
        )


class PokemonUpdateDTOFactory(ModelFactory[PokemonUpdateDTO]):
    __model__ = PokemonUpdateDTO

    @classmethod
    def name_only(cls) -> PokemonUpdateDTO:
        return cls.build(
            name="Updated Name",
            type_primary=None,
            type_secondary=None,
            attacks=None,
            nature=None,
            level=None,
        )

    @classmethod
    def level_only(cls) -> PokemonUpdateDTO:
        return cls.build(
            name=None,
            type_primary=None,
            type_secondary=None,
            attacks=None,
            nature=None,
            level=50,
        )


class PokemonResponseDTOFactory(ModelFactory[PokemonResponseDTO]):
    __model__ = PokemonResponseDTO

    @classmethod
    def from_pokemon(cls, pokemon: Pokemon) -> PokemonResponseDTO:
        return cls.build(
            id=pokemon.id,
            name=pokemon.name,
            type_primary=pokemon.type_primary.value,
            type_secondary=pokemon.type_secondary.value if pokemon.type_secondary else None,
            attacks=pokemon.attacks,
            nature=pokemon.nature.value,
            level=pokemon.level,
        )

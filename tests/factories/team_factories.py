from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from src.application.dtos.team_dto import (
    TeamAddPokemonDTO,
    TeamMemberResponseDTO,
    TeamResponseDTO,
    TeamUpdatePositionDTO,
)
from src.domain.entities.team import Team


class TeamFactory(DataclassFactory[Team]):
    __model__ = Team

    @classmethod
    def ash_pikachu_team_member(cls) -> Team:
        return cls.build(
            id=1,
            trainer_id=1,
            pokemon_id=1,
            position=1,
            is_active=True,
        )

    @classmethod
    def ash_charizard_team_member(cls) -> Team:
        return cls.build(
            id=2,
            trainer_id=1,
            pokemon_id=2,
            position=2,
            is_active=True,
        )

    @classmethod
    def gary_blastoise_team_member(cls) -> Team:
        return cls.build(
            id=3,
            trainer_id=2,
            pokemon_id=3,
            position=1,
            is_active=True,
        )

    @classmethod
    def inactive_team_member(cls) -> Team:
        return cls.build(
            trainer_id=1,
            pokemon_id=4,
            position=3,
            is_active=False,
        )

    @classmethod
    def position_six_member(cls) -> Team:
        return cls.build(
            trainer_id=1,
            pokemon_id=5,
            position=6,
            is_active=True,
        )

    @classmethod
    def invalid_position_high(cls) -> Team:
        return cls.build(position=7)

    @classmethod
    def invalid_position_low(cls) -> Team:
        return cls.build(position=0)

    @classmethod
    def full_team_for_trainer(cls, trainer_id: int) -> list[Team]:
        return [
            cls.build(
                id=i,
                trainer_id=trainer_id,
                pokemon_id=i + 10,
                position=i,
                is_active=True,
            )
            for i in range(1, 7)
        ]


class TeamAddPokemonDTOFactory(ModelFactory[TeamAddPokemonDTO]):
    __model__ = TeamAddPokemonDTO

    @classmethod
    def add_pikachu_to_ash(cls) -> TeamAddPokemonDTO:
        return cls.build(
            trainer_id=1,
            pokemon_id=1,
            position=1,
        )

    @classmethod
    def add_charizard_to_ash(cls) -> TeamAddPokemonDTO:
        return cls.build(
            trainer_id=1,
            pokemon_id=2,
            position=2,
        )

    @classmethod
    def add_to_position_six(cls) -> TeamAddPokemonDTO:
        return cls.build(
            trainer_id=1,
            pokemon_id=6,
            position=6,
        )

    @classmethod
    def invalid_position_high(cls) -> TeamAddPokemonDTO:
        return cls.build(
            trainer_id=1,
            pokemon_id=1,
            position=7,
        )

    @classmethod
    def invalid_position_low(cls) -> TeamAddPokemonDTO:
        return cls.build(
            trainer_id=1,
            pokemon_id=1,
            position=0,
        )

    @classmethod
    def nonexistent_trainer(cls) -> TeamAddPokemonDTO:
        return cls.build(
            trainer_id=999,
            pokemon_id=1,
            position=1,
        )

    @classmethod
    def nonexistent_pokemon(cls) -> TeamAddPokemonDTO:
        return cls.build(
            trainer_id=1,
            pokemon_id=999,
            position=1,
        )


class TeamUpdatePositionDTOFactory(ModelFactory[TeamUpdatePositionDTO]):
    __model__ = TeamUpdatePositionDTO

    @classmethod
    def move_to_position_three(cls) -> TeamUpdatePositionDTO:
        return cls.build(new_position=3)

    @classmethod
    def move_to_position_six(cls) -> TeamUpdatePositionDTO:
        return cls.build(new_position=6)

    @classmethod
    def move_to_position_one(cls) -> TeamUpdatePositionDTO:
        return cls.build(new_position=1)

    @classmethod
    def invalid_position_high(cls) -> TeamUpdatePositionDTO:
        return cls.build(new_position=7)

    @classmethod
    def invalid_position_low(cls) -> TeamUpdatePositionDTO:
        return cls.build(new_position=0)


class TeamMemberResponseDTOFactory(ModelFactory[TeamMemberResponseDTO]):
    __model__ = TeamMemberResponseDTO

    @classmethod
    def pikachu_member(cls) -> TeamMemberResponseDTO:
        return cls.build(
            id=1,
            trainer_id=1,
            pokemon_id=1,
            pokemon_name="Pikachu",
            pokemon_type="electric",
            pokemon_level=25,
            position=1,
            is_active=True,
        )

    @classmethod
    def charizard_member(cls) -> TeamMemberResponseDTO:
        return cls.build(
            id=2,
            trainer_id=1,
            pokemon_id=2,
            pokemon_name="Charizard",
            pokemon_type="fire",
            pokemon_level=36,
            position=2,
            is_active=True,
        )

    @classmethod
    def inactive_member(cls) -> TeamMemberResponseDTO:
        return cls.build(
            trainer_id=1,
            pokemon_id=4,
            pokemon_name="Squirtle",
            pokemon_type="water",
            pokemon_level=15,
            position=3,
            is_active=False,
        )


class TeamResponseDTOFactory(ModelFactory[TeamResponseDTO]):
    __model__ = TeamResponseDTO

    @classmethod
    def ash_team_empty(cls) -> TeamResponseDTO:
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            team_size=0,
            max_size=6,
            members=[],
        )

    @classmethod
    def ash_team_with_pikachu(cls) -> TeamResponseDTO:
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            team_size=1,
            max_size=6,
            members=[TeamMemberResponseDTOFactory.pikachu_member()],
        )

    @classmethod
    def ash_team_with_two_pokemon(cls) -> TeamResponseDTO:
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            team_size=2,
            max_size=6,
            members=[
                TeamMemberResponseDTOFactory.pikachu_member(),
                TeamMemberResponseDTOFactory.charizard_member(),
            ],
        )

    @classmethod
    def full_team(cls) -> TeamResponseDTO:
        members = [
            TeamMemberResponseDTOFactory.build(
                id=i,
                trainer_id=1,
                pokemon_id=i,
                pokemon_name=f"Pokemon{i}",
                pokemon_type="normal",
                pokemon_level=20 + i,
                position=i,
                is_active=True,
            )
            for i in range(1, 7)
        ]
        return cls.build(
            trainer_id=1,
            trainer_name="Ash Ketchum",
            team_size=6,
            max_size=6,
            members=members,
        )

    @classmethod
    def gary_team_empty(cls) -> TeamResponseDTO:
        return cls.build(
            trainer_id=2,
            trainer_name="Gary Oak",
            team_size=0,
            max_size=6,
            members=[],
        )

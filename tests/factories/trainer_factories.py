from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from src.application.dtos.trainer_dto import (
    PokemonSummaryDTO,
    TrainerCreateDTO,
    TrainerResponseDTO,
    TrainerUpdateDTO,
)
from src.domain.entities.trainer import Trainer
from src.domain.enums.trainer_enums import Gender, Region


class TrainerFactory(DataclassFactory[Trainer]):
    __model__ = Trainer

    @classmethod
    def ash_ketchum(cls) -> Trainer:
        return cls.build(
            id=1,
            name="Ash Ketchum",
            gender=Gender.MALE,
            region=Region.KANTO,
            user_id=None,
            username=None,
        )

    @classmethod
    def misty(cls) -> Trainer:
        return cls.build(
            id=2,
            name="Misty",
            gender=Gender.FEMALE,
            region=Region.KANTO,
            user_id=None,
            username=None,
        )

    @classmethod
    def gary_oak(cls) -> Trainer:
        return cls.build(
            id=3,
            name="Gary Oak",
            gender=Gender.MALE,
            region=Region.KANTO,
            user_id=None,
            username=None,
        )

    @classmethod
    def brock(cls) -> Trainer:
        return cls.build(
            id=4,
            name="Brock",
            gender=Gender.MALE,
            region=Region.KANTO,
            user_id=None,
            username=None,
        )

    @classmethod
    def with_user(cls) -> Trainer:
        return cls.build(
            user_id=cls.__faker__.random_int(min=1, max=1000),
            username=cls.__faker__.user_name(),
        )


class TrainerCreateDTOFactory(ModelFactory[TrainerCreateDTO]):
    __model__ = TrainerCreateDTO

    @classmethod
    def ash_ketchum(cls) -> TrainerCreateDTO:
        return cls.build(
            name="Ash Ketchum",
            gender=Gender.MALE,
            region=Region.KANTO,
        )

    @classmethod
    def misty(cls) -> TrainerCreateDTO:
        return cls.build(
            name="Misty",
            gender=Gender.FEMALE,
            region=Region.KANTO,
        )

    @classmethod
    def random_trainer(cls) -> TrainerCreateDTO:
        return cls.build(
            name=cls.__faker__.name(),
            gender=cls.__faker__.enum(Gender),
            region=cls.__faker__.enum(Region),
        )


class TrainerUpdateDTOFactory(ModelFactory[TrainerUpdateDTO]):
    __model__ = TrainerUpdateDTO

    @classmethod
    def name_only(cls) -> TrainerUpdateDTO:
        return cls.build(
            name="Updated Trainer",
            gender=None,
            region=None,
        )

    @classmethod
    def gender_only(cls) -> TrainerUpdateDTO:
        return cls.build(
            name=None,
            gender=Gender.OTHER,
            region=None,
        )

    @classmethod
    def region_only(cls) -> TrainerUpdateDTO:
        return cls.build(
            name=None,
            gender=None,
            region=Region.JOHTO,
        )

    @classmethod
    def full_update(cls) -> TrainerUpdateDTO:
        return cls.build(
            name="Completely Updated Trainer",
            gender=Gender.FEMALE,
            region=Region.HOENN,
        )


class PokemonSummaryDTOFactory(ModelFactory[PokemonSummaryDTO]):
    __model__ = PokemonSummaryDTO

    @classmethod
    def pikachu_summary(cls) -> PokemonSummaryDTO:
        return cls.build(
            id=1,
            name="Pikachu",
            type_primary="electric",
            level=25,
        )

    @classmethod
    def charizard_summary(cls) -> PokemonSummaryDTO:
        return cls.build(
            id=2,
            name="Charizard",
            type_primary="fire",
            level=36,
        )


class TrainerResponseDTOFactory(ModelFactory[TrainerResponseDTO]):
    __model__ = TrainerResponseDTO

    @classmethod
    def from_trainer(cls, trainer: Trainer, pokemon_team: list[PokemonSummaryDTO] | None = None) -> TrainerResponseDTO:
        team = pokemon_team or []
        return cls.build(
            id=trainer.id,
            name=trainer.name,
            gender=trainer.gender.value,
            region=trainer.region.value,
            team_size=len(team),
            pokemon_team=team,
        )

    @classmethod
    def ash_with_team(cls) -> TrainerResponseDTO:
        return cls.build(
            id=1,
            name="Ash Ketchum",
            gender=Gender.MALE.value,
            region=Region.KANTO.value,
            team_size=2,
            pokemon_team=[
                PokemonSummaryDTOFactory.pikachu_summary(),
                PokemonSummaryDTOFactory.charizard_summary(),
            ],
        )

    @classmethod
    def empty_team(cls) -> TrainerResponseDTO:
        return cls.build(
            team_size=0,
            pokemon_team=[],
        )

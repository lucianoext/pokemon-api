from src.application.dtos.trainer_dto import (
    PokemonSummaryDTO,
    TrainerCreateDTO,
    TrainerResponseDTO,
    TrainerUpdateDTO,
)
from src.application.services.base_service import BaseService
from src.domain.entities.trainer import Trainer
from src.domain.repositories.pokemon_repository import PokemonRepository
from src.domain.repositories.team_repository import TeamRepository
from src.domain.repositories.trainer_repository import TrainerRepository


class TrainerService(
    BaseService[Trainer, TrainerCreateDTO, TrainerUpdateDTO, TrainerResponseDTO]
):
    def __init__(
        self,
        trainer_repository: TrainerRepository,
        team_repository: TeamRepository | None = None,
        pokemon_repository: PokemonRepository | None = None,
    ):
        super().__init__(trainer_repository)
        self.team_repository = team_repository
        self.pokemon_repository = pokemon_repository

    def create_trainer(self, trainer_dto: TrainerCreateDTO) -> TrainerResponseDTO:
        return self.create(trainer_dto)

    def get_trainer(self, trainer_id: int) -> TrainerResponseDTO | None:
        return self.get_by_id(trainer_id)

    def get_all_trainers(
        self, skip: int = 0, limit: int = 100
    ) -> list[TrainerResponseDTO]:
        return self.get_all(skip, limit)

    def update_trainer(
        self, trainer_id: int, trainer_dto: TrainerUpdateDTO
    ) -> TrainerResponseDTO | None:
        return self.update(trainer_id, trainer_dto)

    def delete_trainer(self, trainer_id: int) -> bool:
        return self.delete(trainer_id)

    def _dto_to_entity(self, dto: TrainerCreateDTO) -> Trainer:
        return Trainer(
            id=None,
            name=dto.name,
            gender=dto.gender,
            region=dto.region,
        )

    def _transform_to_response_dto(self, trainer: Trainer) -> TrainerResponseDTO:
        pokemon_team = []

        if self.team_repository and self.pokemon_repository and trainer.id:
            team_members = self.team_repository.get_team_by_trainer(trainer.id)

            for team_member in team_members:
                pokemon = self.pokemon_repository.get_by_id(team_member.pokemon_id)
                if pokemon and pokemon.id is not None:
                    pokemon_team.append(
                        PokemonSummaryDTO(
                            id=pokemon.id,
                            name=pokemon.name,
                            type_primary=pokemon.type_primary.value,
                            level=pokemon.level,
                        )
                    )

        return TrainerResponseDTO(
            id=trainer.id,
            name=trainer.name,
            gender=trainer.gender.value,
            region=trainer.region.value,
            team_size=len(pokemon_team),
            pokemon_team=pokemon_team,
        )

    def _apply_update_dto(
        self, existing_trainer: Trainer, dto: TrainerUpdateDTO
    ) -> Trainer:
        non_none_fields = self._get_dto_non_none_fields(dto)

        return Trainer(
            id=existing_trainer.id,
            name=non_none_fields.get("name", existing_trainer.name),
            gender=non_none_fields.get("gender", existing_trainer.gender),
            region=non_none_fields.get("region", existing_trainer.region),
            user_id=existing_trainer.user_id,
            username=existing_trainer.username,
        )

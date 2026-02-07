# src/application/services/trainer_service.py
from src.application.dtos.trainer_dto import (
    TrainerCreateDTO,
    TrainerResponseDTO,
    TrainerUpdateDTO,
)
from src.application.services.base_service import BaseService
from src.domain.entities.trainer import Trainer
from src.domain.repositories.trainer_repository import TrainerRepository


class TrainerService(
    BaseService[Trainer, TrainerCreateDTO, TrainerUpdateDTO, TrainerResponseDTO]
):
    def __init__(self, trainer_repository: TrainerRepository):
        super().__init__(trainer_repository)

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
        return TrainerResponseDTO(
            id=trainer.id,
            name=trainer.name,
            gender=trainer.gender.value,
            region=trainer.region.value,
            team_size=0,
            pokemon_team=[],
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

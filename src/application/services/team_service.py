# src/application/services/team_service.py
from src.application.dtos.team_dto import (
    TeamAddPokemonDTO,
    TeamMemberResponseDTO,
    TeamResponseDTO,
    TeamUpdatePositionDTO,
)
from src.domain.entities.team import Team
from src.domain.exceptions import BusinessRuleException, EntityNotFoundException
from src.domain.repositories.pokemon_repository import PokemonRepository
from src.domain.repositories.team_repository import TeamRepository
from src.domain.repositories.trainer_repository import TrainerRepository


class TeamService:
    def __init__(
        self,
        team_repository: TeamRepository,
        trainer_repository: TrainerRepository,
        pokemon_repository: PokemonRepository,
    ):
        self.team_repository = team_repository
        self.trainer_repository = trainer_repository
        self.pokemon_repository = pokemon_repository

    def add_pokemon_to_team(self, dto: TeamAddPokemonDTO) -> TeamResponseDTO:
        trainer = self.trainer_repository.get_by_id(dto.trainer_id)
        if not trainer:
            raise EntityNotFoundException("Trainer", dto.trainer_id)

        pokemon = self.pokemon_repository.get_by_id(dto.pokemon_id)
        if not pokemon:
            raise EntityNotFoundException("Pokemon", dto.pokemon_id)

        self._validate_add_pokemon_rules(dto)

        team_entry = Team(
            id=None,
            trainer_id=dto.trainer_id,
            pokemon_id=dto.pokemon_id,
            position=dto.position,
            is_active=True,
        )

        self.team_repository.add_pokemon_to_team(team_entry)
        return self.get_trainer_team(dto.trainer_id)

    def remove_pokemon_from_team(
        self, trainer_id: int, pokemon_id: int
    ) -> TeamResponseDTO:
        team_member = self.team_repository.get_team_member(trainer_id, pokemon_id)
        if not team_member:
            raise BusinessRuleException(
                f"Pokemon {pokemon_id} is not in trainer {trainer_id}'s team"
            )

        success = self.team_repository.remove_pokemon_from_team(trainer_id, pokemon_id)
        if not success:
            raise BusinessRuleException("Failed to remove Pokemon from team")

        return self.get_trainer_team(trainer_id)

    def update_pokemon_position(
        self, trainer_id: int, pokemon_id: int, dto: TeamUpdatePositionDTO
    ) -> TeamResponseDTO:
        team_member = self.team_repository.get_team_member(trainer_id, pokemon_id)
        if not team_member:
            raise BusinessRuleException(
                f"Pokemon {pokemon_id} is not in trainer {trainer_id}'s team"
            )

        self._validate_position_available(trainer_id, dto.new_position, pokemon_id)
        self.team_repository.update_position(trainer_id, pokemon_id, dto.new_position)
        return self.get_trainer_team(trainer_id)

    def get_trainer_team(self, trainer_id: int) -> TeamResponseDTO:
        trainer = self.trainer_repository.get_by_id(trainer_id)
        if not trainer:
            raise EntityNotFoundException("Trainer", trainer_id)

        team_members = self.team_repository.get_team_by_trainer(trainer_id)

        member_dtos = []
        for member in team_members:
            pokemon = self.pokemon_repository.get_by_id(member.pokemon_id)
            if pokemon:
                member_dto = TeamMemberResponseDTO(
                    id=member.id,
                    trainer_id=member.trainer_id,
                    pokemon_id=member.pokemon_id,
                    pokemon_name=pokemon.name,
                    pokemon_type=pokemon.type_primary.value,
                    pokemon_level=pokemon.level,
                    position=member.position,
                    is_active=member.is_active,
                )
                member_dtos.append(member_dto)

        return TeamResponseDTO(
            trainer_id=trainer_id,
            trainer_name=trainer.name,
            team_size=len(member_dtos),
            members=member_dtos,
        )

    def _validate_add_pokemon_rules(self, dto: TeamAddPokemonDTO) -> None:
        current_size = self.team_repository.get_trainer_team_size(dto.trainer_id)
        if current_size >= 6:
            raise BusinessRuleException("Maximum 6 Pokemon per team")

        existing_member = self.team_repository.get_team_member(
            dto.trainer_id, dto.pokemon_id
        )
        if existing_member:
            raise BusinessRuleException(
                f"Pokemon {dto.pokemon_id} is already in trainer {dto.trainer_id}'s team"
            )

        self._validate_position_available(dto.trainer_id, dto.position)

    def _validate_position_available(
        self, trainer_id: int, position: int, exclude_pokemon_id: int | None = None
    ) -> None:
        team_members = self.team_repository.get_team_by_trainer(trainer_id)

        for member in team_members:
            if member.position == position and member.pokemon_id != exclude_pokemon_id:
                raise BusinessRuleException(
                    f"Position {position} is already occupied in trainer {trainer_id}'s team"
                )

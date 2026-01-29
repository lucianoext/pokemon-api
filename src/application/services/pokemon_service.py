from typing import List, Optional
from src.application.dtos.pokemon_dto import PokemonCreateDTO, PokemonResponseDTO, PokemonUpdateDTO
from src.domain.entities.pokemon import Pokemon
from src.domain.repositories.pokemon_repository import PokemonRepository
from src.domain import BusinessRuleException

class PokemonService:
    def __init__(self, pokemon_repository: PokemonRepository):
        self.pokemon_repository = pokemon_repository
    
    def create_pokemon(self, dto: PokemonCreateDTO) -> PokemonResponseDTO:
        self._validate_business_rules_for_creation(dto)
        pokemon = self._dto_to_entity(dto)
        created_pokemon = self.pokemon_repository.create(pokemon)
        return self._transform_to_response_dto(created_pokemon)
    
    def get_pokemon(self, pokemon_id: int) -> Optional[PokemonResponseDTO]:
        pokemon = self.pokemon_repository.get_by_id(pokemon_id)
        if not pokemon:
            return None
        return self._transform_to_response_dto(pokemon)
    
    def get_all_pokemon(self, skip: int = 0, limit: int = 100) -> List[PokemonResponseDTO]:
        pokemons = self.pokemon_repository.get_all(skip, limit)
        return [self._transform_to_response_dto(pokemon) for pokemon in pokemons]
    
    def update_pokemon(self, pokemon_id: int, pokemon_dto: PokemonUpdateDTO) -> Optional[PokemonResponseDTO]:
        existing_pokemon = self.pokemon_repository.get_by_id(pokemon_id)
        if not existing_pokemon:
            return None
        
        updated_pokemon = Pokemon(
            id=existing_pokemon.id,
            name=pokemon_dto.name if pokemon_dto.name is not None else existing_pokemon.name,
            type_primary=pokemon_dto.type_primary if pokemon_dto.type_primary is not None else existing_pokemon.type_primary,
            type_secondary=pokemon_dto.type_secondary if pokemon_dto.type_secondary is not None else existing_pokemon.type_secondary,
            attacks=pokemon_dto.attacks if pokemon_dto.attacks is not None else existing_pokemon.attacks,
            nature=pokemon_dto.nature if pokemon_dto.nature is not None else existing_pokemon.nature,
            level=pokemon_dto.level if pokemon_dto.level is not None else existing_pokemon.level
        )
        
        self._validate_business_rules_for_update(updated_pokemon)
        
        saved_pokemon = self.pokemon_repository.update(pokemon_id, updated_pokemon)
        return self._transform_to_response_dto(saved_pokemon)

    def level_up_pokemon(self, pokemon_id: int, levels: int = 1) -> Optional[PokemonResponseDTO]:
        pokemon = self.pokemon_repository.get_by_id(pokemon_id)
        if not pokemon:
            return None
        
        if pokemon.level + levels > 100:
            raise BusinessRuleException("The level cap is 100")
        
        pokemon.level += levels
        updated_pokemon = self.pokemon_repository.update(pokemon_id, pokemon)
        return self._transform_to_response_dto(updated_pokemon)
        
    def learn_new_attack(
        self, 
        pokemon_id: int, 
        new_attack: str,
        replace_attack: Optional[str] = None
    ) -> Optional[PokemonResponseDTO]:
        
        pokemon = self.pokemon_repository.get_by_id(pokemon_id)
        if not pokemon:
            return None
        
        attacks_list = pokemon.attacks.copy() if isinstance(pokemon.attacks, list) else pokemon.attacks
        
        if new_attack in attacks_list:
            raise BusinessRuleException(f"'{pokemon.name}' already knows '{new_attack}'")
        
        if len(attacks_list) >= 4:
            if not replace_attack:
                raise BusinessRuleException(f"'{pokemon.name}' already knows 4 attacks. You must specify which one to replace.")
            
            if replace_attack not in attacks_list:
                raise BusinessRuleException(f"'{pokemon.name}' doesn't know '{replace_attack}'")
            
            attacks_list.remove(replace_attack)
        
        attacks_list.append(new_attack)
        pokemon.attacks = attacks_list
        
        updated_pokemon = self.pokemon_repository.update(pokemon_id, pokemon)
        return self._transform_to_response_dto(updated_pokemon)
        
    def _validate_business_rules_for_creation(self, dto: PokemonCreateDTO) -> None:
        if dto.level < 1 or dto.level > 100:
            raise BusinessRuleException(f"Pokemon level must be between 1 and 100, got: {dto.level}")
        
        attacks_list = dto.attacks if isinstance(dto.attacks, list) else dto.attacks
        
        if dto.level > 30 and len(attacks_list) < 3:
            raise BusinessRuleException("Pokemon above level 30 should know at least 3 attacks")
        
        self._validate_powerful_attacks(attacks_list, dto.level)

    def _validate_business_rules_for_update(self, pokemon: Pokemon) -> None:
        if pokemon.level < 1 or pokemon.level > 100:
            raise BusinessRuleException(f"Pokemon level must be between 1 and 100, got: {pokemon.level}")
        
        attacks_list = pokemon.attacks if isinstance(pokemon.attacks, list) else pokemon.attacks
        
        if pokemon.level > 30 and len(attacks_list) < 3:
            raise BusinessRuleException("Pokemon above level 30 should know at least 3 attacks")
        
        self._validate_powerful_attacks(attacks_list, pokemon.level)
    
    def _validate_powerful_attacks(self, attacks_list: List[str], level: int) -> None:
        powerful_attacks = {
            'Hyper Beam': 50,
            'Solar Beam': 40,
            'Thunder': 25,
            'Blizzard': 35
        }
        
        for attack in attacks_list:
            if attack in powerful_attacks:
                required_level = powerful_attacks[attack]
                if level < required_level:
                    raise BusinessRuleException(f"Attack '{attack}' requires level {required_level}")

    def _dto_to_entity(self, dto: PokemonCreateDTO) -> Pokemon:
        return Pokemon(
            id=None,
            name=dto.name,
            type_primary=dto.type_primary,
            type_secondary=dto.type_secondary,
            attacks=dto.attacks,
            nature=dto.nature,
            level=dto.level
        )

    def _transform_to_response_dto(self, pokemon: Pokemon) -> PokemonResponseDTO:
        return PokemonResponseDTO(
            id=pokemon.id,
            name=pokemon.name,
            type_primary=pokemon.type_primary.value,
            type_secondary=pokemon.type_secondary.value if pokemon.type_secondary else None,
            attacks=pokemon.attacks,
            nature=pokemon.nature.value,
            level=pokemon.level
        )
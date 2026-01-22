from typing import List, Optional
from src.application.dtos.pokemon_dto import PokemonCreateDTO, PokemonResponseDTO, PokemonUpdateDTO
from src.domain.entities import pokemon
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
    
    def _validate_business_rules_for_creation(self, dto: PokemonCreateDTO) -> None:
    
        if dto.level > 30 and len(dto.attacks) < 3:
            raise BusinessRuleException(
                "Level 30 Pokemon 30 should know at least 3 attacks"
            )
        
        powerful_attacks = {
            'Hyper Beam': 50,
            'Solar Beam': 40,
            'Thunder': 25,
            'Blizzard': 35
        }
        
        for attack in dto.attacks:
            if attack in powerful_attacks:
                required_level = powerful_attacks[attack]
                if dto.level < required_level:
                    raise BusinessRuleException(
                        f"Atrack '{attack}' requires lvl {required_level}"
                    )

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

    def get_pokemon(self, pokemon_id: int) -> Optional[PokemonResponseDTO]:
        pokemon = self.pokemon_repository.get_by_id(pokemon_id)   

        if not pokemon:
            return None        
        
        return self._transform_to_response_dto(pokemon)
    
    def get_all_pokemons(self, skip: int = 0, limit: int = 100) -> List[PokemonResponseDTO]
        pokemons = self.pokemon_repository.get_all(skip,limit)
        return[self._transform_to_response_dto(pokemon) for pokemon in pokemons]
    
    def update_pokemon(self, pokemon_id: int, pokemon_dto: PokemonUpdateDTO) -> Optional[PokemonResponseDTO]:
        existing_pokemon = self.pokemon_repository.get_by_id(pokemon_id)

        if not existing_pokemon:
            return None
        
        updated_pokemon = Pokemon(
            id=existing_pokemon.id,
            name=existing_pokemon.name if pokemon_dto.name is not None else existing_pokemon.name,
            type_primary=existing_pokemon.type_primary if pokemon_dto.type_primary is not None else existing_pokemon.type_primary,
            type_secondary=existing_pokemon.type_secondary if pokemon_dto.type_secondary is not None else existing_pokemon.type_secondary,
            attacks=pokemon_dto.attacks if pokemon_dto.attacks is not None else existing_pokemon.attacks,
            nature=pokemon_dto.nature if pokemon_dto.nature is not None else existing_pokemon.nature,
            level=pokemon_dto.level if pokemon_dto.level is not None else existing_pokemon.level
        )

        return updated_pokemon


    def level_up_pokemon(self, pokemon_id: int, levels: int = 1) -> Optional[PokemonResponseDTO]:
        
        pokemon = self.pokemon_repository.get_by_id(pokemon_id)
        if not pokemon:
            return None
        
        if pokemon.level + levels > 100:
            raise BusinessRuleException("The lvl cap is 100")
        
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
        
        if new_attack in pokemon.attacks:
            raise BusinessRuleException(f"'{pokemon.name}' already knows '{new_attack}'")
        
        if len(pokemon.attacks) >= 4:
            if not replace_attack:
                raise BusinessRuleException("'{pokemon.name}' already knows 4 attacks. You must specify which one to replace.")
            
            if replace_attack not in pokemon.attacks:
                raise BusinessRuleException(f"'{pokemon.name}' doesn't know '{replace_attack}'")
            
            pokemon.attacks.remove(replace_attack)
        
        pokemon.attacks.append(new_attack)
        
        updated_pokemon = self.pokemon_repository.update(pokemon_id, pokemon)
        
        return self._transform_to_response_dto(updated_pokemon)
        
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
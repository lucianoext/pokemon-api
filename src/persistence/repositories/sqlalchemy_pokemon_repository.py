import json
from sqlalchemy.orm import Session
from src.domain.repositories.pokemon_repository import PokemonRepository
from src.domain.entities.pokemon import Pokemon, PokemonType, PokemonNature
from src.persistence.database.models import PokemonModel

class SqlAlchemyPokemonRepository(PokemonRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, pokemon: Pokemon) -> Pokemon:
        db_pokemon = PokemonModel(
            name=pokemon.name,
            type_primary=self._get_enum_value(pokemon.type_primary),  # ← CAMBIO
            type_secondary=self._get_enum_value(pokemon.type_secondary) if pokemon.type_secondary else None,  # ← CAMBIO
            attacks=json.dumps(pokemon.attacks),
            nature=self._get_enum_value(pokemon.nature),  # ← CAMBIO
            level=pokemon.level
        )
        
        self.db.add(db_pokemon)
        self.db.commit()
        self.db.refresh(db_pokemon)
        
        return self._model_to_entity(db_pokemon)
    
    def get_by_id(self, pokemon_id: int) -> Pokemon | None:
        db_pokemon = self.db.query(PokemonModel).filter(
            PokemonModel.id == pokemon_id
        ).first()
        
        return self._model_to_entity(db_pokemon) if db_pokemon else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Pokemon]:
        db_pokemons = self.db.query(PokemonModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(pokemon) for pokemon in db_pokemons]
    
    def update(self, pokemon_id: int, pokemon: Pokemon) -> Pokemon | None:
        db_pokemon = self.db.query(PokemonModel).filter(
            PokemonModel.id == pokemon_id
        ).first()
        
        if not db_pokemon:
            return None
        
        db_pokemon.name = pokemon.name
        db_pokemon.type_primary = self._get_enum_value(pokemon.type_primary)
        db_pokemon.type_secondary = self._get_enum_value(pokemon.type_secondary) if pokemon.type_secondary else None
        db_pokemon.attacks = json.dumps(pokemon.attacks)
        db_pokemon.nature = self._get_enum_value(pokemon.nature)
        db_pokemon.level = pokemon.level
        
        self.db.commit()
        self.db.refresh(db_pokemon)
        
        return self._model_to_entity(db_pokemon)
    
    def delete(self, pokemon_id: int) -> bool:
        db_pokemon = self.db.query(PokemonModel).filter(
            PokemonModel.id == pokemon_id
        ).first()
        
        if not db_pokemon:
            return False
        
        self.db.delete(db_pokemon)
        self.db.commit()
        return True
    
    def _model_to_entity(self, model: PokemonModel) -> Pokemon:
        attacks_list = []
        if model.attacks:
            try:
                attacks_list = json.loads(model.attacks)
            except json.JSONDecodeError:
                attacks_list = []
        
        primary_type = PokemonType(model.type_primary)
        
        secondary_type = None
        if model.type_secondary:
            secondary_type = PokemonType(model.type_secondary)
        
        nature = PokemonNature(model.nature)
        
        return Pokemon(
            id=model.id,
            name=model.name,
            type_primary=primary_type,
            type_secondary=secondary_type,
            attacks=attacks_list,
            nature=nature,
            level=model.level,
        )
    
    def _entity_to_model(self, pokemon: Pokemon) -> PokemonModel:
        return PokemonModel(
            id=pokemon.id,
            name=pokemon.name,
            type_primary=self._get_enum_value(pokemon.type_primary),
            type_secondary=self._get_enum_value(pokemon.type_secondary) if pokemon.type_secondary else None,
            attacks=json.dumps(pokemon.attacks),
            nature=self._get_enum_value(pokemon.nature),
        )
    
    def _get_enum_value(self, field) -> str:
        if field is None:
            return None
        if hasattr(field, 'value'):
            return field.value
        else:
            return str(field)
from fastapi import APIRouter, Depends, HTTPException, Query
from http import HTTPStatus
from sqlalchemy.orm import Session

from src.persistence.database import get_database
from src.persistence.repositories.sqlalchemy_pokemon_repository import SqlAlchemyPokemonRepository
from src.application.services.pokemon_service import PokemonService
from src.application.dtos.pokemon_dto import (
    PokemonCreateDTO,
    PokemonUpdateDTO,
    PokemonResponseDTO,
)

router = APIRouter(prefix="/pokemon", tags=["pokemon"])

def get_pokemon_service(db: Session = Depends(get_database)) -> PokemonService:
    pokemon_repository = SqlAlchemyPokemonRepository(db)
    return PokemonService(pokemon_repository)

@router.post("/", response_model=PokemonResponseDTO, status_code=HTTPStatus.CREATED)
def create_pokemon(
    pokemon: PokemonCreateDTO,
    service: PokemonService = Depends(get_pokemon_service)
):
    return service.create_pokemon(pokemon)

@router.get("/{pokemon_id}", response_model=PokemonResponseDTO)
def get_pokemon(
    pokemon_id: int,
    service: PokemonService = Depends(get_pokemon_service)
):
    pokemon = service.get_pokemon(pokemon_id)
    if not pokemon:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Pokemon with id {pokemon_id} not found"
        )
    return pokemon

@router.get("/", response_model=list[PokemonResponseDTO])
def get_pokemon_list(
    skip: int = 0,
    limit: int = 100,
    service: PokemonService = Depends(get_pokemon_service)
):
    return service.get_all_pokemon(skip, limit)

@router.put("/{pokemon_id}", response_model=PokemonResponseDTO)
def update_pokemon(
    pokemon_id: int,
    pokemon: PokemonUpdateDTO,
    service: PokemonService = Depends(get_pokemon_service)
):
    updated_pokemon = service.update_pokemon(pokemon_id, pokemon)
    if not updated_pokemon:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Pokemon with id {pokemon_id} not found"
        )
    return updated_pokemon

@router.delete("/{pokemon_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_pokemon(
    pokemon_id: int,
    service: PokemonService = Depends(get_pokemon_service)
):
    success = service.delete_pokemon(pokemon_id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Pokemon with id {pokemon_id} not found"
        )

@router.post("/{pokemon_id}/level-up", response_model=PokemonResponseDTO)
def level_up_pokemon(
    pokemon_id: int,
    levels: int = 1,
    service: PokemonService = Depends(get_pokemon_service)
):
    try:
        return service.level_up_pokemon(pokemon_id, levels)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{pokemon_id}/learn-attack", response_model=PokemonResponseDTO)
def learn_attack(
    pokemon_id: int,
    new_attack: str,
    replace_attack: str | None = None,
    service: PokemonService = Depends(get_pokemon_service)
):
    try:
        return service.learn_new_attack(pokemon_id, new_attack, replace_attack)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
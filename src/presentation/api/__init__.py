from .trainers import router as trainers_router
from .pokemon import router as pokemon_router
from .teams import router as teams_router

__all__ = ["trainers_router", "pokemon_router", "teams_router"]
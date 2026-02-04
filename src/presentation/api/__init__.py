from .auth import router as auth_router
from .pokemon import router as pokemon_router
from .teams import router as teams_router
from .trainers import router as trainers_router

__all__ = ["trainers_router", "pokemon_router", "teams_router", "auth_router"]

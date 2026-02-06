"""API client package for Pokemon API frontend."""

from typing import Any

from .auth_client import AuthClient
from .backpacks_client import BackpacksClient
from .base_client import BaseAPIClient
from .battles_client import BattlesClient
from .items_client import ItemsClient
from .pokemon_client import PokemonClient
from .teams_client import TeamsClient
from .trainers_client import TrainersClient


class APIClient:
    """Unified API client combining all endpoints."""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1") -> None:
        """Initialize API client with base URL."""
        self.base_url = base_url
        self.base = BaseAPIClient(base_url)
        self.auth = AuthClient(base_url)
        self.trainers = TrainersClient(base_url)
        self.pokemon = PokemonClient(base_url)
        self.teams = TeamsClient(base_url)
        self.items = ItemsClient(base_url)
        self.backpacks = BackpacksClient(base_url)
        self.battles = BattlesClient(base_url)  # ADD THIS

    def __getattr__(self, name: str) -> Any:
        """Delegate method calls to appropriate clients."""
        for client in [
            self.base,
            self.auth,
            self.trainers,
            self.pokemon,
            self.teams,
            self.items,
            self.backpacks,
            self.battles,  # ADD THIS
        ]:
            if hasattr(client, name):
                return getattr(client, name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    # Health check and dashboard stats from base
    def health_check(self) -> dict[str, Any]:
        """Check API health status."""
        result = self.base.health_check()
        return result if isinstance(result, dict) else {"status": "unknown"}

    def get_dashboard_stats(self) -> dict[str, Any]:
        """Get dashboard statistics."""
        result = self.base.get_dashboard_stats()
        return result if isinstance(result, dict) else {}


# Global instance
api_client = APIClient()

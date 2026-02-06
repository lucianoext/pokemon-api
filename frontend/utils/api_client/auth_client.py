"""Authentication API endpoints."""

from typing import Any

import requests

from .base_client import BaseAPIClient


class AuthClient(BaseAPIClient):
    """Authentication API endpoints."""

    def register(self, user_data: dict[str, Any]) -> Any:
        """Register a new user."""
        response = requests.post(
            f"{self.base_url}/auth/register",
            json=user_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def login(self, username: str, password: str) -> Any:
        """Authenticate user."""
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password},
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def get_current_user(self) -> Any:
        """Get current user information."""
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def change_password(self, current_password: str, new_password: str) -> Any:
        """Change user password."""
        response = requests.put(
            f"{self.base_url}/auth/change-password",
            json={"current_password": current_password, "new_password": new_password},
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

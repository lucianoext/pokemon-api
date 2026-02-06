"""Battles API client for Pokemon API frontend."""

from typing import Any, cast

import requests
import streamlit as st

from .base_client import BaseAPIClient


class BattlesClient(BaseAPIClient):
    """Client for battles-related API endpoints."""

    def create_battle(self, battle_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new battle record."""
        response = requests.post(
            f"{self.base_url}/battles",
            json=battle_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return cast(dict[str, Any], self._handle_response(response))

    def get_battles(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get all battles."""
        try:
            response = requests.get(
                f"{self.base_url}/battles",
                params={"skip": skip, "limit": limit},
                headers=self._get_headers(),
                timeout=30,
            )

            if response.status_code == 401:
                st.session_state.authenticated = False
                st.error("Session expired. Please log in again.")
                st.rerun()

            response.raise_for_status()
            data = response.json()
            return cast(list[dict[str, Any]], data if isinstance(data, list) else [])

        except requests.HTTPError:
            if response.status_code == 404:
                return []
            return []
        except Exception:
            return []

    def get_trainer_battles(self, trainer_id: int) -> list[dict[str, Any]]:
        """Get battles for a specific trainer."""
        try:
            response = requests.get(
                f"{self.base_url}/battles/trainer/{trainer_id}",
                headers=self._get_headers(),
                timeout=30,
            )

            if response.status_code == 401:
                st.session_state.authenticated = False
                st.error("Session expired. Please log in again.")
                st.rerun()

            response.raise_for_status()
            data = response.json()
            return cast(list[dict[str, Any]], data if isinstance(data, list) else [])

        except requests.HTTPError:
            return []
        except Exception:
            return []

    def get_leaderboard(self) -> dict[str, Any]:
        """Get battle leaderboard."""
        try:
            response = requests.get(
                f"{self.base_url}/battles/leaderboard",
                headers=self._get_headers(),
                timeout=30,
            )

            if response.status_code == 401:
                st.session_state.authenticated = False
                st.error("Session expired. Please log in again.")
                st.rerun()

            response.raise_for_status()
            return cast(dict[str, Any], response.json())

        except Exception:
            return {"leaderboard": [], "total_trainers": 0, "total_battles": 0}

    def delete_battle(self, battle_id: int) -> bool:
        """Delete a battle record."""
        try:
            response = requests.delete(
                f"{self.base_url}/battles/{battle_id}",
                headers=self._get_headers(),
                timeout=30,
            )

            if response.status_code == 401:
                st.session_state.authenticated = False
                st.error("Session expired. Please log in again.")
                st.rerun()

            response.raise_for_status()
            return True

        except Exception:
            return False

"""Teams API endpoints."""

from typing import Any

import requests
import streamlit as st

from .base_client import BaseAPIClient


class TeamsClient(BaseAPIClient):
    """Teams API endpoints."""

    def get_teams(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get list of teams."""
        try:
            response = requests.get(
                f"{self.base_url}/teams",
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
            return data if isinstance(data, list) else []

        except requests.HTTPError as e:
            if response.status_code == 404:
                return []
            st.error(f"API Error loading teams: {e}")
            return []
        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Error loading teams: {str(e)}")
            return []

    def get_team(self, team_id: int) -> Any:
        """Get team by ID."""
        response = requests.get(
            f"{self.base_url}/teams/{team_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def create_team(self, team_data: dict[str, Any]) -> Any:
        """Create new team."""
        response = requests.post(
            f"{self.base_url}/teams",
            json=team_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def update_team(self, team_id: int, team_data: dict[str, Any]) -> Any:
        """Update team."""
        response = requests.put(
            f"{self.base_url}/teams/{team_id}",
            json=team_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def delete_team(self, team_id: int) -> None:
        """Delete team."""
        response = requests.delete(
            f"{self.base_url}/teams/{team_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

    def add_pokemon_to_team(self, team_data: dict[str, Any]) -> Any:
        """Add pokemon to team."""
        response = requests.post(
            f"{self.base_url}/teams/add-pokemon",
            json=team_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def remove_pokemon_from_team(self, trainer_id: int, pokemon_id: int) -> Any:
        """Remove pokemon from team."""
        response = requests.delete(
            f"{self.base_url}/teams/trainers/{trainer_id}/pokemon/{pokemon_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def update_pokemon_position(
        self, trainer_id: int, pokemon_id: int, new_position: int
    ) -> Any:
        """Update pokemon position in team."""
        response = requests.put(
            f"{self.base_url}/teams/trainers/{trainer_id}/pokemon/{pokemon_id}/position",
            json={"new_position": new_position},
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def get_trainer_team(self, trainer_id: int) -> Any:
        """Get trainer's team."""
        response = requests.get(
            f"{self.base_url}/teams/trainers/{trainer_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def _get_trainers_list(self) -> list[dict[str, Any]]:
        """Internal method to get trainers list."""
        try:
            response = requests.get(
                f"{self.base_url}/trainers",
                params={"skip": 0, "limit": 1000},
                headers=self._get_headers(),
                timeout=30,
            )

            if response.status_code == 401:
                st.session_state.authenticated = False
                st.error("Session expired. Please log in again.")
                st.rerun()

            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []

        except requests.HTTPError:
            if response.status_code == 404:
                return []
            return []
        except Exception:  # pylint: disable=broad-exception-caught
            return []

    def get_all_teams(self, _skip: int = 0, _limit: int = 100) -> list[dict[str, Any]]:
        """Get all teams by fetching all trainers and their teams."""
        try:
            trainers = self._get_trainers_list()
            teams = []

            for trainer in trainers:
                try:
                    team = self.get_trainer_team(trainer["id"])
                    if team and team.get("members"):
                        teams.append(team)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(
                        f"Warning: Could not load team for trainer {trainer.get('id')}: {e}"
                    )

            return teams

        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Error loading teams: {str(e)}")
            return []

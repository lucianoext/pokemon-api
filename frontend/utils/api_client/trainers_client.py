"""Trainers API endpoints."""

from typing import Any

import requests
import streamlit as st

from .base_client import BaseAPIClient


class TrainersClient(BaseAPIClient):
    """Trainers API endpoints."""

    def get_trainers(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get list of trainers."""
        try:
            response = requests.get(
                f"{self.base_url}/trainers",
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
            st.error(f"API Error loading trainers: {e}")
            return []
        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Error loading trainers: {str(e)}")
            return []

    def get_trainer(self, trainer_id: int) -> Any:
        """Get trainer by ID."""
        response = requests.get(
            f"{self.base_url}/trainers/{trainer_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def create_trainer(self, trainer_data: dict[str, Any]) -> Any:
        """Create new trainer."""
        response = requests.post(
            f"{self.base_url}/trainers",
            json=trainer_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def update_trainer(self, trainer_id: int, trainer_data: dict[str, Any]) -> Any:
        """Update trainer."""
        response = requests.put(
            f"{self.base_url}/trainers/{trainer_id}",
            json=trainer_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def delete_trainer(self, trainer_id: int) -> None:
        """Delete trainer."""
        response = requests.delete(
            f"{self.base_url}/trainers/{trainer_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

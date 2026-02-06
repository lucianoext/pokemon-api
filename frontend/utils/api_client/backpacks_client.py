"""Backpacks API endpoints."""

from typing import Any

import requests
import streamlit as st

from .base_client import BaseAPIClient


class BackpacksClient(BaseAPIClient):
    """Backpacks API endpoints."""

    def get_backpacks(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get list of backpacks."""
        try:
            response = requests.get(
                f"{self.base_url}/backpacks",
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
            st.error(f"API Error loading backpacks: {e}")
            return []
        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Error loading backpacks: {str(e)}")
            return []

    def get_backpack(self, backpack_id: int) -> Any:
        """Get backpack by ID."""
        response = requests.get(
            f"{self.base_url}/backpacks/{backpack_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def create_backpack(self, backpack_data: dict[str, Any]) -> Any:
        """Create new backpack entry."""
        response = requests.post(
            f"{self.base_url}/backpacks",
            json=backpack_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def update_backpack(self, backpack_id: int, backpack_data: dict[str, Any]) -> Any:
        """Update backpack entry."""
        response = requests.put(
            f"{self.base_url}/backpacks/{backpack_id}",
            json=backpack_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def delete_backpack(self, backpack_id: int) -> None:
        """Delete backpack entry."""
        response = requests.delete(
            f"{self.base_url}/backpacks/{backpack_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

    def add_item_to_backpack(self, backpack_data: dict[str, Any]) -> Any:
        """Add item to backpack."""
        response = requests.post(
            f"{self.base_url}/backpacks/add-item",
            json=backpack_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def remove_item_from_backpack(
        self, trainer_id: int, item_id: int, quantity: int
    ) -> Any:
        """Remove item from backpack."""
        response = requests.delete(
            f"{self.base_url}/backpacks/trainers/{trainer_id}/items/{item_id}",
            json={"quantity": quantity},
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def update_item_quantity(
        self, trainer_id: int, item_id: int, new_quantity: int
    ) -> Any:
        """Update item quantity in backpack."""
        response = requests.put(
            f"{self.base_url}/backpacks/trainers/{trainer_id}/items/{item_id}/quantity",
            json={"new_quantity": new_quantity},
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def get_trainer_backpack(self, trainer_id: int) -> Any:
        """Get trainer's backpack."""
        response = requests.get(
            f"{self.base_url}/backpacks/trainers/{trainer_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def clear_trainer_backpack(self, trainer_id: int) -> Any:
        """Clear trainer's backpack."""
        response = requests.delete(
            f"{self.base_url}/backpacks/trainers/{trainer_id}/clear",
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

    def get_all_backpacks(
        self,
        _skip: int = 0,
        _limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get all backpacks by fetching all trainers and their backpacks."""
        try:
            trainers = self._get_trainers_list()
            backpacks = []

            for trainer in trainers:
                try:
                    backpack = self.get_trainer_backpack(trainer["id"])
                    if backpack and backpack.get("items"):
                        backpacks.append(backpack)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(
                        f"Warning: Could not load backpack for trainer {trainer.get('id')}: {e}"
                    )

            return backpacks

        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Error loading backpacks: {str(e)}")
            return []

"""Items API endpoints."""

from typing import Any

import requests
import streamlit as st

from .base_client import BaseAPIClient


class ItemsClient(BaseAPIClient):
    """Items API endpoints."""

    def get_items(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get list of items."""
        try:
            response = requests.get(
                f"{self.base_url}/items",
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
            st.error(f"API Error loading items: {e}")
            return []
        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Error loading items: {str(e)}")
            return []

    def get_item(self, item_id: int) -> Any:
        """Get item by ID."""
        response = requests.get(
            f"{self.base_url}/items/{item_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def create_item(self, item_data: dict[str, Any]) -> Any:
        """Create new item."""
        response = requests.post(
            f"{self.base_url}/items",
            json=item_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def update_item(self, item_id: int, item_data: dict[str, Any]) -> Any:
        """Update item."""
        response = requests.put(
            f"{self.base_url}/items/{item_id}",
            json=item_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def delete_item(self, item_id: int) -> None:
        """Delete item."""
        response = requests.delete(
            f"{self.base_url}/items/{item_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

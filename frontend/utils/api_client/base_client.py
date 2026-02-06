"""Base API client with common functionality."""

import json
from typing import Any

import requests
import streamlit as st


class BaseAPIClient:
    """Base client with common API functionality."""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1") -> None:
        """Initialize API client with base URL."""
        self.base_url = base_url

    def _get_headers(self) -> dict[str, str]:
        """Get headers with authentication token if available."""
        headers = {"Content-Type": "application/json"}
        if "access_token" in st.session_state:
            headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        return headers

    def _handle_response(self, response: requests.Response) -> Any:
        """Handle API response with error checking."""
        if response.status_code == 401:
            st.error("Session expired. Please log in again.")
            st.session_state.authenticated = False
            st.rerun()

        if not response.ok:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except (ValueError, KeyError, json.JSONDecodeError):
                error_detail = f"HTTP {response.status_code} - {response.text[:100]}"
            raise requests.HTTPError(f"Error {response.status_code}: {error_detail}")

        try:
            return response.json()
        except (ValueError, json.JSONDecodeError):
            return {"error": "Invalid JSON response", "text": response.text}

    def health_check(self) -> Any:
        """Check API health status."""
        try:
            response = requests.get("http://localhost:8000/health", timeout=10)
            if response.ok:
                return response.json()

            return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
        except requests.RequestException as e:
            return {"status": "unhealthy", "error": str(e)}

    def _get_trainers_for_stats(self) -> list[dict[str, Any]]:
        """Internal method to get trainers for dashboard stats."""
        try:
            response = requests.get(
                f"{self.base_url}/trainers",
                params={"skip": 0, "limit": 100},
                headers=self._get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except Exception:  # pylint: disable=broad-exception-caught
            return []

    def _get_pokemon_for_stats(self) -> list[dict[str, Any]]:
        """Internal method to get pokemon for dashboard stats."""
        try:
            response = requests.get(
                f"{self.base_url}/pokemon",
                params={"skip": 0, "limit": 100},
                headers=self._get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except Exception:  # pylint: disable=broad-exception-caught
            return []

    def _get_items_for_stats(self) -> list[dict[str, Any]]:
        """Internal method to get items for dashboard stats."""
        try:
            response = requests.get(
                f"{self.base_url}/items",
                params={"skip": 0, "limit": 100},
                headers=self._get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except Exception:  # pylint: disable=broad-exception-caught
            return []

    def get_dashboard_stats(self) -> dict[str, Any]:
        """Get dashboard statistics."""
        try:
            stats = {
                "trainers_count": 0,
                "pokemon_count": 0,
                "items_count": 0,
                "average_level": 0.0,
                "error": False,
            }

            try:
                trainers = self._get_trainers_for_stats()
                stats["trainers_count"] = len(trainers)
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Warning: Could not load trainers data: {e}")

            try:
                pokemon = self._get_pokemon_for_stats()
                stats["pokemon_count"] = len(pokemon)
                if pokemon:
                    levels = [p.get("level", 1) for p in pokemon]
                    stats["average_level"] = sum(levels) / len(levels)
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Warning: Could not load pokemon data: {e}")

            try:
                items = self._get_items_for_stats()
                stats["items_count"] = len(items)
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Warning: Could not load items data: {e}")

            return stats

        except Exception as e:  # pylint: disable=broad-exception-caught
            return {"error": True, "message": str(e)}

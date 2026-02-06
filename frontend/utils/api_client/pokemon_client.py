"""Pokemon API endpoints."""

from typing import Any

import requests
import streamlit as st

from .base_client import BaseAPIClient


class PokemonClient(BaseAPIClient):
    """Pokemon API endpoints."""

    def get_pokemon(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get list of pokemon."""
        try:
            response = requests.get(
                f"{self.base_url}/pokemon",
                params={"skip": skip, "limit": limit},
                headers=self._get_headers(),
                timeout=30,
            )

            if response.status_code == 401:
                st.session_state.authenticated = False
                st.error("Session expired. Please log in again.")
                st.rerun()

            if not response.ok:
                if response.status_code == 404:
                    return []

                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", f"HTTP {response.status_code}")
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"Warning: Could not parse error response: {e}")
                    error_msg = f"HTTP {response.status_code}"

                st.error(f"API Error: {error_msg}")
                return []

            try:
                pokemon_data = response.json()

                if not isinstance(pokemon_data, list):
                    return []

                processed_pokemon = []
                for pokemon in pokemon_data:
                    processed = {
                        "id": pokemon.get("id"),
                        "name": pokemon.get("name", ""),
                        "type_primary": pokemon.get("type_primary", "normal"),
                        "type_secondary": pokemon.get("type_secondary"),
                        "nature": pokemon.get("nature", "hardy"),
                        "level": pokemon.get("level", 1),
                        "attacks": pokemon.get("attacks", []),
                    }
                    processed_pokemon.append(processed)

                return processed_pokemon

            except Exception as json_error:  # pylint: disable=broad-exception-caught
                st.error(f"Error processing Pokemon data: {str(json_error)}")
                return []

        except requests.ConnectionError:
            st.error("Cannot connect to Pokemon API. Check if the backend is running.")
            return []
        except requests.Timeout:
            st.error("Request timed out. Please try again.")
            return []
        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Unexpected error loading Pokemon: {str(e)}")
            return []

    def get_pokemon_by_id(self, pokemon_id: int) -> Any:
        """Get pokemon by ID."""
        response = requests.get(
            f"{self.base_url}/pokemon/{pokemon_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def create_pokemon(self, pokemon_data: dict[str, Any]) -> Any:
        """Create new pokemon."""
        response = requests.post(
            f"{self.base_url}/pokemon",
            json=pokemon_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def update_pokemon(self, pokemon_id: int, pokemon_data: dict[str, Any]) -> Any:
        """Update pokemon."""
        response = requests.put(
            f"{self.base_url}/pokemon/{pokemon_id}",
            json=pokemon_data,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def delete_pokemon(self, pokemon_id: int) -> None:
        """Delete pokemon."""
        response = requests.delete(
            f"{self.base_url}/pokemon/{pokemon_id}",
            headers=self._get_headers(),
            timeout=30,
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

    def level_up_pokemon(self, pokemon_id: int, levels: int = 1) -> Any:
        """Level up a pokemon."""
        response = requests.post(
            f"{self.base_url}/pokemon/{pokemon_id}/level-up",
            params={"levels": levels},
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def learn_attack(
        self, pokemon_id: int, new_attack: str, replace_attack: str | None = None
    ) -> Any:
        """Teach a new attack to pokemon."""
        params = {"new_attack": new_attack}
        if replace_attack:
            params["replace_attack"] = replace_attack

        response = requests.post(
            f"{self.base_url}/pokemon/{pokemon_id}/learn-attack",
            params=params,
            headers=self._get_headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def get_pokemon_types(self) -> list[str]:
        """Get list of available pokemon types."""
        return [
            "normal",
            "fire",
            "water",
            "electric",
            "grass",
            "ice",
            "fighting",
            "poison",
            "ground",
            "flying",
            "psychic",
            "bug",
            "rock",
            "ghost",
            "dragon",
            "dark",
            "steel",
            "fairy",
        ]

    def get_pokemon_natures(self) -> list[str]:
        """Get list of available pokemon natures."""
        return [
            "hardy",
            "lonely",
            "brave",
            "adamant",
            "naughty",
            "bold",
            "docile",
            "relaxed",
            "impish",
            "lax",
            "timid",
            "hasty",
            "serious",
            "jolly",
            "naive",
            "modest",
            "mild",
            "quiet",
            "bashful",
            "rash",
            "calm",
            "gentle",
            "sassy",
            "careful",
            "quirky",
        ]

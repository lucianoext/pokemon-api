from typing import Any

import requests
import streamlit as st


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1") -> None:
        self.base_url = base_url
        self.session = requests.Session()

    def _get_headers(self) -> dict[str, str]:
        """Get headers with token if authenticated"""
        headers = {"Content-Type": "application/json"}
        if "access_token" in st.session_state:
            headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        return headers

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        """Handle API response"""
        if response.status_code == 401:
            # Token expired
            if "access_token" in st.session_state:
                del st.session_state.access_token
                del st.session_state.user_info
                st.session_state.authenticated = False
            st.error("🔒 Session expired. Please log in again.")
            st.session_state.current_page = "auth"
            st.rerun()

        if not response.ok:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except (ValueError, requests.exceptions.JSONDecodeError):
                error_detail = f"HTTP Error {response.status_code}"
            raise requests.HTTPError(error_detail)

        response_data: dict[str, Any] = response.json()
        return response_data

    # ==============================
    # AUTH ENDPOINTS
    # ==============================

    def register(self, user_data: dict[str, Any]) -> dict[str, Any]:
        """Register a new user"""
        response = self.session.post(
            f"{self.base_url}/auth/register",
            json=user_data,
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def login(self, username: str, password: str) -> dict[str, Any]:
        """Login user"""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password},
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def get_current_user(self) -> dict[str, Any]:
        """Get current user information"""
        response = self.session.get(
            f"{self.base_url}/auth/me", headers=self._get_headers()
        )
        return self._handle_response(response)

    def change_password(
        self, current_password: str, new_password: str
    ) -> dict[str, Any]:
        """Change password"""
        response = self.session.put(
            f"{self.base_url}/auth/change-password",
            json={"current_password": current_password, "new_password": new_password},
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    # ==============================
    # TRAINERS ENDPOINTS
    # ==============================

    def get_trainers(self, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get list of trainers"""
        response = self.session.get(
            f"{self.base_url}/trainers",
            params={"skip": skip, "limit": limit},
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def get_trainer(self, trainer_id: int) -> dict[str, Any]:
        """Get trainer by ID"""
        response = self.session.get(
            f"{self.base_url}/trainers/{trainer_id}", headers=self._get_headers()
        )
        return self._handle_response(response)

    def create_trainer(self, trainer_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new trainer"""
        response = self.session.post(
            f"{self.base_url}/trainers", json=trainer_data, headers=self._get_headers()
        )
        return self._handle_response(response)

    def update_trainer(
        self, trainer_id: int, trainer_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a trainer"""
        response = self.session.put(
            f"{self.base_url}/trainers/{trainer_id}",
            json=trainer_data,
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def delete_trainer(self, trainer_id: int) -> None:
        """Delete a trainer"""
        response = self.session.delete(
            f"{self.base_url}/trainers/{trainer_id}", headers=self._get_headers()
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

    # ==============================
    # POKEMON ENDPOINTS
    # ==============================

    def get_pokemon(self, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get list of pokemon"""
        response = self.session.get(
            f"{self.base_url}/pokemon",
            params={"skip": skip, "limit": limit},
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def get_pokemon_by_id(self, pokemon_id: int) -> dict[str, Any]:
        """Get pokemon by ID"""
        response = self.session.get(
            f"{self.base_url}/pokemon/{pokemon_id}", headers=self._get_headers()
        )
        return self._handle_response(response)

    def create_pokemon(self, pokemon_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new pokemon"""
        response = self.session.post(
            f"{self.base_url}/pokemon", json=pokemon_data, headers=self._get_headers()
        )
        return self._handle_response(response)

    def update_pokemon(
        self, pokemon_id: int, pokemon_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a pokemon"""
        response = self.session.put(
            f"{self.base_url}/pokemon/{pokemon_id}",
            json=pokemon_data,
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def delete_pokemon(self, pokemon_id: int) -> None:
        """Delete a pokemon"""
        response = self.session.delete(
            f"{self.base_url}/pokemon/{pokemon_id}", headers=self._get_headers()
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

    def search_pokemon(
        self,
        name: str | None = None,
        type_primary: str | None = None,
        nature: str | None = None,
        min_level: int | None = None,
        max_level: int | None = None,
    ) -> dict[str, Any]:
        """Search pokemon with filters"""
        params = {}
        if name:
            params["name"] = name
        if type_primary:
            params["type_primary"] = type_primary
        if nature:
            params["nature"] = nature
        if min_level is not None:
            params["min_level"] = str(min_level)
        if max_level is not None:
            params["max_level"] = str(max_level)

        response = self.session.get(
            f"{self.base_url}/pokemon/search",
            params=params,
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    # ==============================
    # TEAMS ENDPOINTS
    # ==============================

    def get_teams(self, trainer_id: int | None = None) -> dict[str, Any]:
        """Get teams, optionally filtered by trainer"""
        params = {}
        if trainer_id:
            params["trainer_id"] = trainer_id

        response = self.session.get(
            f"{self.base_url}/teams", params=params, headers=self._get_headers()
        )
        return self._handle_response(response)

    def get_team(self, team_id: int) -> dict[str, Any]:
        """Get team by ID"""
        response = self.session.get(
            f"{self.base_url}/teams/{team_id}", headers=self._get_headers()
        )
        return self._handle_response(response)

    def create_team(self, team_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new team (add pokemon to trainer team)"""
        response = self.session.post(
            f"{self.base_url}/teams", json=team_data, headers=self._get_headers()
        )
        return self._handle_response(response)

    def update_team(self, team_id: int, team_data: dict[str, Any]) -> dict[str, Any]:
        """Update a team"""
        response = self.session.put(
            f"{self.base_url}/teams/{team_id}",
            json=team_data,
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def delete_team_member(self, team_id: int) -> None:
        """Remove a pokemon from team"""
        response = self.session.delete(
            f"{self.base_url}/teams/{team_id}", headers=self._get_headers()
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

    def get_trainer_team(self, trainer_id: int) -> dict[str, Any]:
        """Get complete team of a trainer"""
        response = self.session.get(
            f"{self.base_url}/teams/trainer/{trainer_id}", headers=self._get_headers()
        )
        return self._handle_response(response)

    # ==============================
    # ITEMS ENDPOINTS
    # ==============================

    def get_items(self, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get list of items"""
        response = self.session.get(
            f"{self.base_url}/items",
            params={"skip": skip, "limit": limit},
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def get_item(self, item_id: int) -> dict[str, Any]:
        """Get item by ID"""
        response = self.session.get(
            f"{self.base_url}/items/{item_id}", headers=self._get_headers()
        )
        return self._handle_response(response)

    def create_item(self, item_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new item"""
        response = self.session.post(
            f"{self.base_url}/items", json=item_data, headers=self._get_headers()
        )
        return self._handle_response(response)

    def update_item(self, item_id: int, item_data: dict[str, Any]) -> dict[str, Any]:
        """Update an item"""
        response = self.session.put(
            f"{self.base_url}/items/{item_id}",
            json=item_data,
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def delete_item(self, item_id: int) -> None:
        """Delete an item"""
        response = self.session.delete(
            f"{self.base_url}/items/{item_id}", headers=self._get_headers()
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

    def search_items(
        self,
        name: str | None = None,
        item_type: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
    ) -> dict[str, Any]:
        """Search items with filters"""
        params = {}
        if name:
            params["name"] = name
        if item_type:
            params["type"] = item_type
        if min_price is not None:
            params["min_price"] = str(min_price)
        if max_price is not None:
            params["max_price"] = str(max_price)

        response = self.session.get(
            f"{self.base_url}/items/search", params=params, headers=self._get_headers()
        )
        return self._handle_response(response)

    # ==============================
    # BACKPACKS ENDPOINTS
    # ==============================

    def get_backpacks(self, trainer_id: int | None = None) -> dict[str, Any]:
        """Get backpacks, optionally filtered by trainer"""
        params = {}
        if trainer_id:
            params["trainer_id"] = trainer_id

        response = self.session.get(
            f"{self.base_url}/backpacks", params=params, headers=self._get_headers()
        )
        return self._handle_response(response)

    def get_backpack(self, backpack_id: int) -> dict[str, Any]:
        """Get backpack entry by ID"""
        response = self.session.get(
            f"{self.base_url}/backpacks/{backpack_id}", headers=self._get_headers()
        )
        return self._handle_response(response)

    def create_backpack_entry(self, backpack_data: dict[str, Any]) -> dict[str, Any]:
        """Create new backpack entry (add item to backpack)"""
        response = self.session.post(
            f"{self.base_url}/backpacks",
            json=backpack_data,
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def update_backpack_entry(
        self, backpack_id: int, backpack_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update backpack entry (change quantity)"""
        response = self.session.put(
            f"{self.base_url}/backpacks/{backpack_id}",
            json=backpack_data,
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def delete_backpack_entry(self, backpack_id: int) -> None:
        """Delete backpack entry"""
        response = self.session.delete(
            f"{self.base_url}/backpacks/{backpack_id}", headers=self._get_headers()
        )
        if response.status_code not in [200, 204]:
            self._handle_response(response)

    def get_trainer_backpack(self, trainer_id: int) -> dict[str, Any]:
        """Get complete backpack of a trainer"""
        response = self.session.get(
            f"{self.base_url}/backpacks/trainer/{trainer_id}",
            headers=self._get_headers(),
        )
        return self._handle_response(response)

    def add_item_to_backpack(
        self, trainer_id: int, item_id: int, quantity: int = 1
    ) -> dict[str, Any]:
        """Add item to trainer's backpack"""
        backpack_data = {
            "trainer_id": trainer_id,
            "item_id": item_id,
            "quantity": quantity,
        }
        return self.create_backpack_entry(backpack_data)

    def remove_item_from_backpack(
        self, trainer_id: int, item_id: int, quantity: int = 1
    ) -> dict[str, Any]:
        """Remove quantity of item from backpack"""
        # First get current entry
        backpack_response = self.get_trainer_backpack(trainer_id)
        backpack_entries: list[dict[str, Any]] = (
            backpack_response if isinstance(backpack_response, list) else []
        )
        entry = next((e for e in backpack_entries if e["item_id"] == item_id), None)

        if not entry:
            raise ValueError("Item not found in backpack")

        new_quantity = entry["quantity"] - quantity

        if new_quantity <= 0:
            # Remove completely
            self.delete_backpack_entry(entry["id"])
            return {"message": "Item removed from backpack"}
        else:
            # Update quantity
            return self.update_backpack_entry(entry["id"], {"quantity": new_quantity})

    # ==============================
    # UTILITY METHODS
    # ==============================

    def health_check(self) -> dict[str, Any]:
        """Check if API is available"""
        try:
            response = self.session.get(
                f"{self.base_url.replace('/api/v1', '')}/health"
            )
            health_data: dict[str, Any] = response.json()
            return health_data
        except Exception as e:
            return {"status": "error", "detail": str(e)}

    def get_api_version(self) -> dict[str, Any]:
        """Get API version"""
        try:
            response = self.session.get(
                f"{self.base_url.replace('/api/v1', '')}/version"
            )
            version_data: dict[str, Any] = response.json()
            return version_data
        except Exception as e:
            return {"version": "unknown", "error": str(e)}

    # ==============================
    # BULK OPERATIONS
    # ==============================

    def bulk_create_pokemon(self, pokemon_list: list[dict[str, Any]]) -> dict[str, Any]:
        """Create multiple pokemon in batch"""
        results: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []

        for i, pokemon_data in enumerate(pokemon_list):
            try:
                result = self.create_pokemon(pokemon_data)
                results.append(result)
            except Exception as e:
                errors.append({"index": i, "data": pokemon_data, "error": str(e)})

        return {
            "created": results,
            "errors": errors,
            "total_processed": len(pokemon_list),
            "success_count": len(results),
            "error_count": len(errors),
        }

    def bulk_create_items(self, items_list: list[dict[str, Any]]) -> dict[str, Any]:
        """Create multiple items in batch"""
        results: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []

        for i, item_data in enumerate(items_list):
            try:
                result = self.create_item(item_data)
                results.append(result)
            except Exception as e:
                errors.append({"index": i, "data": item_data, "error": str(e)})

        return {
            "created": results,
            "errors": errors,
            "total_processed": len(items_list),
            "success_count": len(results),
            "error_count": len(errors),
        }

    # ==============================
    # STATISTICS METHODS
    # ==============================

    def get_dashboard_stats(self) -> dict[str, Any]:
        """Get statistics for dashboard"""
        try:
            stats: dict[str, Any] = {}

            # Count trainers
            trainers_response = self.get_trainers(limit=1000)
            trainers: list[dict[str, Any]] = (
                trainers_response if isinstance(trainers_response, list) else []
            )
            stats["trainers_count"] = len(trainers)

            # Count pokemon
            pokemon_response = self.get_pokemon(limit=1000)
            pokemon: list[dict[str, Any]] = (
                pokemon_response if isinstance(pokemon_response, list) else []
            )
            stats["pokemon_count"] = len(pokemon)

            # Count items
            items_response = self.get_items(limit=1000)
            items: list[dict[str, Any]] = (
                items_response if isinstance(items_response, list) else []
            )
            stats["items_count"] = len(items)

            # Pokemon statistics
            if pokemon:
                stats["average_level"] = sum(p.get("level", 1) for p in pokemon) / len(
                    pokemon
                )
                stats["max_level"] = max(p.get("level", 1) for p in pokemon)
                stats["min_level"] = min(p.get("level", 1) for p in pokemon)

                # Most common types
                types = [p.get("type_primary") for p in pokemon]
                type_counts: dict[str, int] = {}
                for ptype in types:
                    if ptype:
                        type_counts[ptype] = type_counts.get(ptype, 0) + 1
                stats["most_common_types"] = sorted(
                    type_counts.items(), key=lambda x: x[1], reverse=True
                )[:5]

            # Trainer statistics
            if trainers:
                regions = [t.get("region") for t in trainers]
                region_counts: dict[str, int] = {}
                for region in regions:
                    if region:
                        region_counts[region] = region_counts.get(region, 0) + 1
                stats["trainers_by_region"] = region_counts

                # Total pokemon in teams
                stats["total_team_pokemon"] = sum(
                    t.get("team_size", 0) for t in trainers
                )

            return stats

        except Exception as e:
            return {"error": str(e)}


# Global client instance
api_client = APIClient()

"""Form validators for Pokemon API frontend."""

import json


class FormValidators:
    """Utility class for form validation."""

    @staticmethod
    def validate_pokemon_name(name: str) -> tuple[bool, str]:
        """Validate pokemon name."""
        if not name or len(name.strip()) == 0:
            return False, "Pokemon name is required"
        if len(name) > 50:
            return False, "Pokemon name must be 50 characters or less"
        return True, ""

    @staticmethod
    def validate_trainer_name(name: str) -> tuple[bool, str]:
        """Validate trainer name."""
        if not name or len(name.strip()) == 0:
            return False, "Trainer name is required"
        if len(name) > 100:
            return False, "Trainer name must be 100 characters or less"
        return True, ""

    @staticmethod
    def validate_item_name(name: str) -> tuple[bool, str]:
        """Validate item name."""
        if not name or len(name.strip()) == 0:
            return False, "Item name is required"
        if len(name) > 50:
            return False, "Item name must be 50 characters or less"
        return True, ""

    @staticmethod
    def validate_price(price: int) -> tuple[bool, str]:
        """Validate item price."""
        if price < 0:
            return False, "Price cannot be negative"
        if price > 999999:
            return False, "Price cannot exceed 999,999"
        return True, ""

    @staticmethod
    def validate_level(level: int) -> tuple[bool, str]:
        """Validate pokemon level."""
        if level < 1:
            return False, "Level must be at least 1"
        if level > 100:
            return False, "Level cannot exceed 100"
        return True, ""

    @staticmethod
    def validate_quantity(quantity: int) -> tuple[bool, str]:
        """Validate item quantity."""
        if quantity < 0:
            return False, "Quantity cannot be negative"
        if quantity > 999:
            return False, "Quantity cannot exceed 999"
        return True, ""

    @staticmethod
    def validate_json_attacks(attacks_str: str) -> tuple[bool, str]:
        """Validate attacks JSON string."""
        if not attacks_str.strip():
            return True, ""  # Empty is OK

        try:
            attacks = json.loads(attacks_str)
            if not isinstance(attacks, list):
                return False, "Attacks must be a JSON list"
            if len(attacks) > 4:
                return False, "Pokemon cannot have more than 4 attacks"
            for attack in attacks:
                if not isinstance(attack, str):
                    return False, "All attacks must be strings"
            return True, ""
        except json.JSONDecodeError:
            return False, "Invalid JSON format"

    @staticmethod
    def get_pokemon_types() -> list[str]:
        """Get list of valid pokemon types."""
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

    @staticmethod
    def get_pokemon_natures() -> list[str]:
        """Get list of valid pokemon natures."""
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

    @staticmethod
    def get_trainer_genders() -> list[str]:
        """Get list of valid trainer genders."""
        return ["male", "female", "other"]

    @staticmethod
    def get_trainer_regions() -> list[str]:
        """Get list of valid trainer regions."""
        return [
            "kanto",
            "johto",
            "hoenn",
            "sinnoh",
            "unova",
            "kalos",
            "alola",
            "galar",
            "paldea",
        ]

    @staticmethod
    def get_item_types() -> list[str]:
        """Get list of valid item types."""
        return [
            "pokeball",
            "potion",
            "berry",
            "tm",
            "evolution",
            "battle",
            "key",
            "misc",
        ]

from dataclasses import dataclass

from src.domain.enums.pokemon_enums import PokemonNature, PokemonType


@dataclass
class Pokemon:
    id: int | None
    name: str
    type_primary: PokemonType
    type_secondary: PokemonType | None
    attacks: list[str]
    nature: PokemonNature
    level: int = 1

    def __post_init__(self) -> None:
        if isinstance(self.type_primary, str):
            self.type_primary = PokemonType(self.type_primary)
        if isinstance(self.type_secondary, str):
            self.type_secondary = PokemonType(self.type_secondary)
        if isinstance(self.nature, str):
            self.nature = PokemonNature(self.nature)

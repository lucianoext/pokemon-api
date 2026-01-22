from typing import Optional
from dataclasses import dataclass
from enum import Enum

class PokemonType(Enum):
    NORMAL = "normal"
    FIRE = "fire"
    WATER = "water"
    ELECTRIC = "electric"
    GRASS = "grass"
    ICE = "ice"
    FIGHTING = "fighting"
    POISON = "poison"
    GROUND = "ground"
    FLYING = "flying"
    PSYCHIC = "psychic"
    BUG = "bug"
    ROCK = "rock"
    GHOST = "ghost"
    DRAGON = "dragon"
    DARK = "dark"
    STEEL = "steel"
    FAIRY = "fairy"

class PokemonNature(Enum):
    HARDY = "hardy"
    LONELY = "lonely"
    BRAVE = "brave"
    ADAMANT = "adamant"
    NAUGHTY = "naughty"
    BOLD = "bold"
    DOCILE = "docile"
    RELAXED = "relaxed"
    IMPISH = "impish"
    LAX = "lax"
    TIMID = "timid"
    HASTY = "hasty"
    SERIOUS = "serious"
    JOLLY = "jolly"
    NAIVE = "naive"
    MODEST = "modest"
    MILD = "mild"
    QUIET = "quiet"
    BASHFUL = "bashful"
    RASH = "rash"
    CALM = "calm"
    GENTLE = "gentle"
    SASSY = "sassy"
    CAREFUL = "careful"
    QUIRKY = "quirky"

@dataclass
class Pokemon:
    id: Optional[int]
    name: str
    type_primary: PokemonType
    type_secondary: Optional[PokemonType]
    attacks: str
    nature: PokemonNature
    level: int = 1
    
    def __post_init__(self):
        if isinstance(self.type_primary, str):
            self.type_primary = PokemonType(self.type_primary)
        if isinstance(self.type_secondary, str):
            self.type_secondary = PokemonType(self.type_secondary)
        if isinstance(self.nature, str):
            self.nature = PokemonNature(self.nature)
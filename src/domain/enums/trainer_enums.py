from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Region(str, Enum):
    KANTO = "kanto"
    JOHTO = "johto"
    HOENN = "hoenn"
    SINNOH = "sinnoh"
    UNOVA = "unova"
    KALOS = "kalos"
    ALOLA = "alola"
    GALAR = "galar"

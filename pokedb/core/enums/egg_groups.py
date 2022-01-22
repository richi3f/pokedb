__all__ = ["EggGroup"]

from enum import auto

from pokedb.core.enums.base import IntEnum


class EggGroup(IntEnum):
    MONSTER = auto()
    WATER_1 = auto()
    BUG = auto()
    FLYING = auto()
    FIELD = auto()
    FAIRY = auto()
    GRASS = auto()
    HUMAN__LIKE = auto()
    WATER_3 = auto()
    MINERAL = auto()
    AMORPHOUS = auto()
    WATER_2 = auto()
    DITTO = auto()
    DRAGON = auto()
    UNDISCOVERED = auto()

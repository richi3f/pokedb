__all__ = ["ExperienceGroup"]

from pokedb.core.enums.base import StrEnum


class ExperienceGroup(StrEnum):
    ERRATIC = "Erratic"
    FAST = "Fast"
    MEDIUM_FAST = "Medium Fast"
    MEDIUM_SLOW = "Medium Slow"
    SLOW = "Slow"
    FLUCTUATING = "Fluctuating"

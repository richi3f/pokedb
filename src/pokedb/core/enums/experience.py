__all__ = ["ExperienceGroup"]

from enum import Enum


class ExperienceGroup(Enum):
    ERRATIC = "Erratic"
    FAST = "Fast"
    MEDIUM_FAST = "Medium Fast"
    MEDIUM_SLOW = "Medium Slow"
    SLOW = "Slow"
    FLUCTUATING = "Fluctuating"

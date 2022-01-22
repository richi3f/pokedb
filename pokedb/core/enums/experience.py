__all__ = ["ExperienceGroup"]

from enum import Enum


class ExperienceGroup(Enum):
    ERRATIC = "Erratic"
    FAST = "Fast"
    MEDIUM_FAST = "Medium Fast"
    MEDIUM_SLOW = "Medium Slow"
    SLOW = "Slow"
    FLUCTUATING = "Fluctuating"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, value) -> "ExperienceGroup":
        return cls._value2member_map_[value]

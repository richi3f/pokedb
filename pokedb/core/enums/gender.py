__all__ = ["Gender"]

from enum import Enum
from typing import Any

from pokedb.core.enums.base import StrEnum


class Gender(StrEnum):
    MALE = "md"
    FEMALE = "fd"
    MALE_OR_FEMALE = "mf"
    MALE_ONLY = "mo"
    FEMALE_ONLY = "fo"
    UNKNOWN = "uk"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, value) -> Any:
        return cls._value2member_map_[value]

__all__ = ["Gender"]

from enum import Enum
from typing import Any


class Gender(Enum):
    Male = "md"
    Female = "fd"
    MaleOrFemale = "mf"
    MaleOnly = "mo"
    FemaleOnly = "fo"
    Unknown = "uk"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, value) -> Any:
        return cls._value2member_map_[value]

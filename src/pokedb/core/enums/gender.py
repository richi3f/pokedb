__all__ = ["Gender"]

from enum import Enum


class Gender(Enum):
    MALE = "md"
    FEMALE = "fd"
    MALE_OR_FEMALE = "mf"
    MALE_ONLY = "mo"
    FEMALE_ONLY = "fo"
    UNKNOWN = "uk"

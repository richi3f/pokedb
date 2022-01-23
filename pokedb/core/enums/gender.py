__all__ = ["Gender"]

from pokedb.core.enums.base import StrEnum


class Gender(StrEnum):
    MALE = "md"
    FEMALE = "fd"
    MALE_OR_FEMALE = "mf"
    MALE_ONLY = "mo"
    FEMALE_ONLY = "fo"
    UNKNOWN = "uk"

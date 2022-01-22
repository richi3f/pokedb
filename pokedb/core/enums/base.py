__all__ = ["IntEnum", "StrEnum"]

import enum

FROM_STR_TRANS = str.maketrans({" ": "_", "-": "__"})
TO_STR_TRANS = str.maketrans({"_": None})


class IntEnum(enum.IntEnum):
    def __str__(self) -> str:
        return self._name_.translate(TO_STR_TRANS).lower()

    @classmethod
    def from_str(cls, string: str) -> "IntEnum":
        return cls[string.translate(FROM_STR_TRANS).upper()]


class StrEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, value) -> "StrEnum":
        return cls._value2member_map_[value]

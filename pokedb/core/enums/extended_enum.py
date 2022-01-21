__all__ = ["ExtendedEnum"]

from enum import IntEnum

FROM_STR_TRANS = str.maketrans({" ": "_", "-": "__"})
TO_STR_TRANS = str.maketrans({"_": None})


class ExtendedEnum(IntEnum):
    def __str__(self) -> str:
        return self._name_.translate(TO_STR_TRANS).lower()

    @classmethod
    def from_str(cls, string: str):
        return cls[string.translate(FROM_STR_TRANS).upper()]

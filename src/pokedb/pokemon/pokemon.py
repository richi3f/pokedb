__all__ = ["Pokemon"]

import re
from dataclasses import dataclass

from pokedb.core.enums import Color, EggGroup, ExperienceGroup, Gender, Type


MEGA_PATTERN = re.compile(r"Mega (\w+)(?: X| Y)?")


@dataclass
class Pokemon:
    base_id: int = None
    form_id: int = None
    slug: str = None
    name: str = None
    form_name: str = None
    pokemon_type: tuple[Type, Type] = ()
    egg_group: tuple[EggGroup, EggGroup] = ()
    gender: tuple[Gender] = ()
    gender_ratio: int = None
    has_gigantamax: bool = False
    is_sublegendary: bool = False
    is_legendary: bool = False
    is_mythical: bool = False
    is_baby: bool = False
    color: Color = None
    experience_group: ExperienceGroup = None
    generation: int = None
    evolution_ids: tuple[tuple[int, int], ...] = ()

    @property
    def base_form_index(self) -> tuple[int, int]:
        return self.base_id, 0

    @property
    def index(self) -> tuple[int, int]:
        return self.base_id, self.form_id

    @property
    def is_mega(self) -> bool:
        return MEGA_PATTERN.fullmatch(self.name) is not None

    def __lt__(self, other: "Pokemon") -> bool:
        return self.base_id < other.base_id and self.form_id < other.base_id

    def __repr__(self) -> str:
        suffix = "" if not self.form_name else f" ({self.form_name})"
        return f"{self.name}{suffix}"

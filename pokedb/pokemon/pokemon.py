__all__ = ["Pokemon"]

import re
from dataclasses import dataclass, field

from pokedb.pokemon.database import PokemonDatabase


MEGA_PATTERN = re.compile(r"Mega (\w+)(?: X| Y)?")


@dataclass
class Pokemon:
    base_id: int
    form_id: int
    slug: str = None
    name: str = None
    form_name: str = None
    egg_groups: tuple = None
    generation: int = None
    genders: tuple = None
    gender_ratio: int = None
    types: tuple = None
    egg_group: str = None
    has_gigantamax: bool = False
    is_sublegendary: bool = False
    is_legendary: bool = False
    is_mythical: bool = False
    is_baby: bool = False
    color: int = None

    def __post_init__(self) -> None:
        PokemonDatabase[(self.base_id, self.form_id)] = self
        self._evolutions = []

    @property
    def evolutions(self) -> tuple:
        return tuple(PokemonDatabase[idx] for idx in self._evolutions)

    @property
    def is_mega(self) -> bool:
        return MEGA_PATTERN.fullmatch(self.name) is not None

    def __repr__(self) -> str:
        suffix = "" if self.form_name is None else f" ({self.form_name})"
        return f"{self.name}{suffix}"

__all__ = ["Pokemon"]

import re
from dataclasses import asdict, dataclass, field
from enum import Enum

from pokedb.pokemon.database import PokemonDatabase

MEGA_PATTERN = re.compile(r"Mega (\w+)(?: X| Y)?")


@dataclass
class Pokemon:
    base_id: int
    form_id: int
    slug: str = None
    name: str = None
    form_name: str = None
    egg_group: tuple = None
    generation: int = None
    gender: tuple = None
    gender_ratio: int = None
    pokemon_type: tuple = None
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
    def evolutions(self) -> tuple["Pokemon", ...]:
        return tuple(PokemonDatabase[idx] for idx in self._evolutions)

    @property
    def is_mega(self) -> bool:
        return MEGA_PATTERN.fullmatch(self.name) is not None

    def __repr__(self) -> str:
        suffix = "" if self.form_name is None else f" ({self.form_name})"
        return f"{self.name}{suffix}"

    def to_dict(self) -> tuple[dict, list]:
        # Create Pokémon dictionary
        pokemon = asdict(self)
        for key, value in list(pokemon.items()):
            if isinstance(value, tuple):
                pokemon.pop(key)
                pokemon[f"{key}_1"] = str(value[0])
                if len(value) > 1:
                    pokemon[f"{key}_2"] = str(value[1])
            elif isinstance(value, Enum):
                pokemon[key] = str(value)
        pokemon["is_mega"] = self.is_mega
        # Create evolution dictionaries
        evolutions = []
        for evolution in self.evolutions:
            evolutions.append(
                {
                    "base_id": self.base_id,
                    "form_id": self.form_id,
                    "evo_base_id": evolution.base_id,
                    "evo_form_id": evolution.form_id,
                }
            )
        return pokemon, evolutions

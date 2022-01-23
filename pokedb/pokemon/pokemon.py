__all__ = ["Pokemon"]

import re
from dataclasses import asdict, dataclass
from enum import Enum

MEGA_PATTERN = re.compile(r"Mega (\w+)(?: X| Y)?")


@dataclass
class Pokemon:
    base_id: int = None
    form_id: int = None
    slug: str = None
    name: str = None
    form_name: str = None
    pokemon_type: tuple = ()
    egg_group: tuple = ()
    gender: tuple = ()
    gender_ratio: int = None
    has_gigantamax: bool = False
    is_sublegendary: bool = False
    is_legendary: bool = False
    is_mythical: bool = False
    is_baby: bool = False
    color: int = None
    experience_group: Enum = None
    generation: int = None

    def __post_init__(self) -> None:
        self._evolutions: list["Pokemon"] = []

    @property
    def evolutions(self) -> tuple["Pokemon", ...]:
        return tuple(self._evolutions)

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
        # Create evolution dictionaries
        evolutions = []
        for evolution in self.evolutions:
            evolutions.append(
                {
                    "base_id": self.base_id,
                    "form_id": self.form_id,
                    "evolution_base_id": evolution.base_id,
                    "evolution_form_id": evolution.form_id,
                }
            )
        return pokemon, evolutions

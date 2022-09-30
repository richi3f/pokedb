__all__ = [
    "DualType",
    "PathLike",
    "PokemonBaseAndFormIndex",
    "PokemonEggGroup",
    "PokemonIndex",
    "PokemonIndexOrSlug",
    "PokemonType",
    "PokemonValue",
    "SingleOrDualType",
    "SingleType",
]

import os
from typing import TYPE_CHECKING, Union

from pokedb.core.enums import EggGroup, Type

if TYPE_CHECKING:
    from pokedb.pokemon.pokemon import Pokemon

EmptyTuple = tuple[()]
PathLike = Union[str, bytes, os.PathLike]

PokemonBaseAndFormIndex = tuple[int, int]
PokemonIndex = Union[int, PokemonBaseAndFormIndex]
PokemonIndexOrSlug = Union[str, PokemonIndex]
PokemonValue = Union["Pokemon", PokemonIndexOrSlug]

SingleType = tuple[Type]
DualType = tuple[Type, Type]
SingleOrDualType = Union[SingleType, DualType]
PokemonType = Union[EmptyTuple, SingleOrDualType]

PokemonEggGroup = Union[EmptyTuple, tuple[EggGroup, EggGroup]]

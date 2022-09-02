__all__ = [
    "DualType",
    "PathLike",
    "PokemonBaseAndFormIndex",
    "PokemonIndex",
    "PokemonIndexOrSlug",
    "PokemonValue",
    "SingleOrDualType",
]

import os
from typing import TYPE_CHECKING, Union

from pokedb.core.enums.pokemon_type import Type

if TYPE_CHECKING:
    from pokedb.pokemon.pokemon import Pokemon

PathLike = Union[str, bytes, os.PathLike]
PokemonBaseAndFormIndex = tuple[int, int]
PokemonIndex = Union[int, PokemonBaseAndFormIndex]
PokemonIndexOrSlug = Union[str, PokemonIndex]
PokemonValue = Union["Pokemon", PokemonIndexOrSlug]

DualType = tuple[Type, Type]
SingleOrDualType = Union[Type, DualType]

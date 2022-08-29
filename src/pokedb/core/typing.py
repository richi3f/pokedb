__all__ = ["PathLike", "PokemonIndex", "PokemonIndexOrSlug"]

import os
from typing import Union

PathLike = Union[str, bytes, os.PathLike]
PokemonIndex = Union[int, tuple[int, int]]
PokemonIndexOrSlug = Union[str, PokemonIndex]

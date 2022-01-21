__all__ = ["PokemonDatabase"]

import pokedb


class _PokemonDatabase(metaclass=pokedb.core.Singleton):
    def __init__(self) -> None:
        self._dict = {}

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            return self._dict[idx]
        elif isinstance(idx, int):
            return self._dict[(idx, 0)]
        else:
            raise IndexError("Index must be int or tuple of ints.")

    def __setitem__(self, idx, pokemon):
        if not isinstance(idx, tuple):
            raise IndexError("Index must be a tuple.")
        if not isinstance(pokemon, pokedb.Pokemon):
            raise ValueError("Can only store Pokemon.")
        self._dict[idx] = pokemon


PokemonDatabase = _PokemonDatabase()

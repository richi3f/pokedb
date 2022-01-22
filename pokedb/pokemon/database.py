__all__ = ["PokemonDatabase"]

from pokedb.core.singleton import Singleton


class _PokemonDatabase(metaclass=Singleton):
    def __init__(self) -> None:
        self._dict = {}

    def get_by_slug(self, slug):
        matches = self.query(lambda pokemon: pokemon.slug == slug)
        if len(matches) < 1:
            raise KeyError(f"Pokémon {slug} was not found in the database.")
        return matches[0]

    def query(self, search_function) -> list:
        return [pokemon for pokemon in self._dict.values() if search_function(pokemon)]

    def __iter__(self):
        return (
            pokemon
            for _, pokemon in sorted(
                self._dict.items(), key=lambda kvp: (kvp[0][0], kvp[0][1])
            )
        )

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            return self._dict[idx]
        elif isinstance(idx, int):
            return self._dict[(idx, 0)]
        else:
            raise IndexError("Index must be int or tuple of ints.")

    def __setitem__(self, idx, pokemon) -> None:
        if not isinstance(idx, tuple):
            raise IndexError("Index must be a tuple.")
        if pokemon.__class__.__name__ != "Pokemon":
            raise ValueError("Can only store Pokemon.")
        self._dict[idx] = pokemon

    def __len__(self) -> int:
        return len(self._dict)


PokemonDatabase = _PokemonDatabase()

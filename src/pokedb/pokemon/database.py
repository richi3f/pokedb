from typing import TYPE_CHECKING, Callable, Iterator

from pokedb.core.singleton import Singleton
from pokedb.core.typing import PokemonIndex, PokemonIndexOrSlug, PokemonValue

if TYPE_CHECKING:
    from pokedb.pokemon.pokemon import Pokemon


class PokemonDatabase(metaclass=Singleton):
    def __init__(self) -> None:
        self._dict: dict[tuple[int, int], "Pokemon"] = {}

    def __iter__(self) -> Iterator["Pokemon"]:
        return iter(sorted(self._dict.values()))

    def __getitem__(self, index: PokemonIndexOrSlug) -> "Pokemon":
        if isinstance(index, str):
            return self.get_by_slug(index)
        index = self._validate_index(index)
        return self._dict[index]

    def __setitem__(self, index: PokemonIndex, pokemon: "Pokemon") -> None:
        if isinstance(index, int):
            index = (index, 0)
        if not isinstance(index, tuple):
            raise IndexError("Index must be a tuple.")
        if pokemon.__class__.__name__ != "Pokemon":
            raise ValueError("Can only store Pokemon.")
        self._dict[index] = pokemon

    def __len__(self) -> int:
        return len(self._dict)

    def _validate_index(self, index: PokemonIndexOrSlug) -> tuple[int, int]:
        if isinstance(index, str):
            return self.get_by_slug(index).index
        if isinstance(index, int):
            return self._validate_index((index, 0))
        assert isinstance(index, tuple) and len(index) == 2
        assert all([isinstance(num, int) for num in index])
        return index

    def remove(self, value: PokemonValue) -> None:
        if value.__class__.__name__ == "Pokemon":
            value = value.index
        value = self._validate_index(value)
        if value not in self._dict:
            return
        self._dict.pop(value)

    def get_by_slug(self, slug: str) -> "Pokemon":
        matches = self.query(lambda pokemon: pokemon.slug == slug)
        if len(matches) < 1:
            raise KeyError(f"Pokémon {slug} was not found in the database.")
        return matches[0]

    def query(self, search_function: Callable[["Pokemon"], bool]) -> list["Pokemon"]:
        return [pokemon for pokemon in self._dict.values() if search_function(pokemon)]

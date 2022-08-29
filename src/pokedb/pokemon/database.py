
from typing import Callable, Iterator, TYPE_CHECKING

from pokedb.core.typing import PokemonIndex, PokemonIndexOrSlug
from pokedb.core.singleton import Singleton

if TYPE_CHECKING:
    from pokedb.pokemon.pokemon import Pokemon


class PokemonDatabase(metaclass=Singleton):
    def __init__(self) -> None:
        self._dict: dict[tuple[int, int], "Pokemon"] = {}

    def __iter__(self) -> Iterator["Pokemon"]:
        return iter(sorted(self._dict.values()))

    def __getitem__(self, idx: PokemonIndexOrSlug) -> "Pokemon":
        if isinstance(idx, str):
            return self.get_by_slug(idx)
        idx = self._validate_index(idx)
        return self._dict[idx]

    def __setitem__(self, idx: PokemonIndex, pokemon: "Pokemon") -> None:
        if isinstance(idx, int):
            idx = (idx, 0)
        if not isinstance(idx, tuple):
            raise IndexError("Index must be a tuple.")
        if pokemon.__class__.__name__ != "Pokemon":
            raise ValueError("Can only store Pokemon.")
        self._dict[idx] = pokemon

    def __len__(self) -> int:
        return len(self._dict)

    def _validate_index(self, idx: PokemonIndexOrSlug) -> tuple[int, int]:
        if isinstance(idx, str):
            return self.get_by_slug(idx).index
        if isinstance(idx, int):
            return self._validate_index((idx, 0))
        assert isinstance(idx, tuple) and len(idx) == 2
        assert all([isinstance(num, int) for num in idx])
        return idx

    def remove(self, idx: PokemonIndexOrSlug) -> None:
        idx = self._validate_index(idx)
        if idx not in self._dict:
            return
        removed_pokemon = self._dict.pop(idx)
        for pokemon in self:
            if removed_pokemon in pokemon.evolutions:
                pokemon._evolutions.remove(removed_pokemon)

    def get_by_slug(self, slug: str) -> "Pokemon":
        matches = self.query(lambda pokemon: pokemon.slug == slug)
        if len(matches) < 1:
            raise KeyError(f"Pokémon {slug} was not found in the database.")
        return matches[0]

    def query(self, search_function: Callable[["Pokemon"], bool]) -> list["Pokemon"]:
        return [pokemon for pokemon in self._dict.values() if search_function(pokemon)]

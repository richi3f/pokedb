__all__ = ["PokemonDatabase"]

from operator import attrgetter
from typing import Any, Callable, Generator, Iterator

from pokedb.core.singleton import Singleton
from pokedb.core.typing import (
    PokemonBaseAndFormIndex,
    PokemonIndex,
    PokemonIndexOrSlug,
    PokemonValue,
)
from pokedb.pokemon.pokemon import Pokemon


class PokemonDatabase(metaclass=Singleton):
    def __init__(self) -> None:
        self._dict: dict[tuple[int, int], Pokemon] = {}

    def __iter__(self) -> Iterator[Pokemon]:
        return iter(sorted(self._dict.values(), key=attrgetter("index")))

    def __getitem__(self, index: PokemonIndexOrSlug) -> Pokemon:
        if isinstance(index, str):
            return self.get_by_slug(index)
        index = self._validate_index(index)
        return self._dict[index]

    def __setitem__(self, index: PokemonIndex, pokemon: Pokemon) -> None:
        if isinstance(index, int):
            index = (index, 0)
        if not isinstance(index, tuple):
            raise IndexError("Index must be a tuple.")
        if not isinstance(pokemon, Pokemon):
            raise ValueError("Can only store Pokemon.")
        self._dict[index] = pokemon

    def __len__(self) -> int:
        return len(self._dict)

    def _validate_index(self, value: PokemonValue) -> PokemonBaseAndFormIndex:
        if isinstance(value, Pokemon):
            return value.index
        if isinstance(value, str):
            return self.get_by_slug(value).index
        if isinstance(value, int):
            return self._validate_index((value, 0))
        assert isinstance(value, tuple) and len(value) == 2
        assert all([isinstance(num, int) for num in value])
        return value

    def remove(self, value: PokemonValue) -> None:
        if isinstance(value, Pokemon):
            value = value.index
        else:
            value = self._validate_index(value)
        if value not in self._dict:
            return
        self._dict.pop(value)

    def get_by_slug(self, slug: str) -> Pokemon:
        matches = self.query(lambda pokemon: pokemon.slug == slug)
        if len(matches) < 1:
            raise KeyError(f"Pokémon {slug} was not found in the database.")
        return matches[0]

    def get_evolution_chain(self, value: PokemonValue) -> list[list[Pokemon]]:
        def _generator(
            index: PokemonBaseAndFormIndex,
            evolutions: list[Pokemon],
        ) -> Generator[list[Pokemon], None, None]:
            if self._dict[index].evolution_ids:
                for evolution_index in self._dict[index].evolution_ids:
                    yield from _generator(
                        evolution_index, evolutions + [self._dict[index]]
                    )
            else:
                yield evolutions + [self._dict[index]]

        index = self._validate_index(value)
        return [*_generator(index, [])]

    def get_forms(self, value: PokemonValue) -> list[Pokemon]:
        base_id, _ = self._validate_index(value)
        return self.query(lambda pokemon: pokemon.base_id == base_id)

    def query(self, search_function: Callable[[Pokemon], bool]) -> list[Pokemon]:
        return [pokemon for pokemon in self if search_function(pokemon)]

    def list_attr(
        self, search_function: Callable[[Pokemon], bool], attr: str
    ) -> list[Any]:
        return [getattr(pokemon, attr) for pokemon in self.query(search_function)]

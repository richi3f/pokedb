__all__ = ["VersionData"]

import bisect
from dataclasses import dataclass, field
from operator import itemgetter
from typing import Iterator

from pokedb.core.typing import PokemonBaseAndFormIndex, PokemonValue
from pokedb.pokemon.database import PokemonDatabase
from pokedb.pokemon.pokemon import Pokemon

_database = PokemonDatabase()


@dataclass
class VersionData:
    slug: str = None
    exclusives: list[PokemonBaseAndFormIndex] = field(default_factory=list)

    def _validate_pokemon(self, value: PokemonValue) -> PokemonBaseAndFormIndex:
        index = value.index if isinstance(value, Pokemon) else value
        return _database._validate_index(index)

    def __contains__(self, value: PokemonValue) -> bool:
        index = self._validate_pokemon(value)
        return index in self.exclusives

    def __iter__(self) -> Iterator[Pokemon]:
        return iter(itemgetter(*self.exclusives)(_database))

    def __len__(self) -> int:
        return len(self.exclusives)

    def add(self, value: PokemonValue) -> None:
        index = self._validate_pokemon(value)
        if index in self:
            raise ValueError("Pokémon is already in version exclusive data.")
        bisect.insort(self.exclusives, index)

    def remove(self, value: PokemonValue) -> None:
        index = self._validate_pokemon(value)
        self.exclusives.remove(index)

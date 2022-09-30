__all__ = ["Pokedex"]

from dataclasses import dataclass, field
from typing import Optional

from pokedb.core.typing import PokemonBaseAndFormIndex, PokemonValue
from pokedb.pokemon.database import PokemonDatabase
from pokedb.pokemon.pokemon import Pokemon


@dataclass
class Pokedex:
    slug: Optional[str] = None
    name: Optional[str] = None
    order: dict[int, list[PokemonBaseAndFormIndex]] = field(default_factory=dict)

    def __getitem__(self, dex_index: int) -> list[Pokemon]:
        if dex_index in self.order:
            database = PokemonDatabase()
            return database.query(
                lambda pokemon: pokemon.index in self.order[dex_index]
            )
        raise KeyError("Index not in Pokédex.")

    def _validate_pokemon(self, value: PokemonValue) -> tuple[int, int]:
        idx = value.index if isinstance(value, Pokemon) else value
        database = PokemonDatabase()
        return database._validate_index(idx)

    def __setitem__(self, dex_index: int, value: PokemonValue) -> None:
        if not isinstance(dex_index, int):
            raise IndexError("Pokédex index must be an int.")
        if value in self:
            raise ValueError(f"{value} is already in Pokédex.")
        index = self._validate_pokemon(value)
        if dex_index not in self.order:
            self.order[dex_index] = []
        self.order[dex_index].append(index)

    def __contains__(self, value: PokemonValue) -> bool:
        try:
            self.indexof(value)
            return True
        except KeyError:
            return False

    def indexof(self, value: PokemonValue) -> int:
        index = self._validate_pokemon(value)
        for dex_index, pokemon_ids in self.order.items():
            try:
                pokemon_ids.index(index)
            except ValueError:
                continue
            return dex_index
        raise KeyError(f"{value} is not part of {self.name}.")

    def __len__(self) -> int:
        return sum(map(len, self.order.values()))

    def __repr__(self) -> str:
        return f"{self.name} ({len(self)} Pokémon)"

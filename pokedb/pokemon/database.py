__all__ = ["PokemonDatabase"]

import csv
from typing import TYPE_CHECKING, Callable, Union

import pandas as pd

from pokedb import io
from pokedb.core.singleton import Singleton

if TYPE_CHECKING:
    from pokedb import Pokemon


class PokemonDatabase(metaclass=Singleton):
    def __init__(self) -> None:
        self._dict = {}

    def get_by_slug(self, slug: str) -> "Pokemon":
        matches = self.query(lambda pokemon: pokemon.slug == slug)
        if len(matches) < 1:
            raise KeyError(f"Pokémon {slug} was not found in the database.")
        return matches[0]

    def query(self, search_function: Callable[["Pokemon"], bool]) -> list:
        return [pokemon for pokemon in self._dict.values() if search_function(pokemon)]

    def __iter__(self):
        return iter(sorted(self._dict.values()))

    def __getitem__(self, idx: Union[int, tuple[int, int]]) -> "Pokemon":
        if isinstance(idx, tuple):
            return self._dict[idx]
        elif isinstance(idx, int):
            return self._dict[(idx, 0)]
        else:
            raise IndexError("Index must be int or tuple of ints.")

    def __setitem__(self, idx: tuple[int, int], pokemon: "Pokemon") -> None:
        if not isinstance(idx, tuple):
            raise IndexError("Index must be a tuple.")
        if pokemon.__class__.__name__ != "Pokemon":
            raise ValueError("Can only store Pokemon.")
        self._dict[idx] = pokemon

    def __len__(self) -> int:
        return len(self._dict)

    def to_json(self, file_path) -> None:
        data = {}
        entry: "Pokemon"
        for entry in self:
            pokemon = {
                "id": entry.base_id,
                "form_id": entry.form_id,
                "name": entry.name,
                "type": [*map(str, entry.pokemon_type)],
                "genders": [*map(str, entry.gender)],
                "gender_ratio": entry.gender_ratio,
                "gen": entry.generation,
                "egg": [*map(str, entry.egg_group)],
                "exp": str(entry.experience_group),
            }
            if entry.form_name:
                pokemon["form"] = entry.form_name
            if entry.color is not None:
                pokemon["color"] = str(entry.color)
            if entry.is_baby:
                pokemon["baby"] = True
            if entry.is_legendary:
                pokemon["legendary"] = True
            if entry.is_sublegendary:
                pokemon["sublegendary"] = True
            if entry.is_mythical:
                pokemon["mythical"] = True
            if entry.is_mega:
                pokemon["mega"] = True
            if entry.has_gigantamax:
                pokemon["gmax"] = True
            if not entry.evolutions:
                pokemon["fully_evolved"] = True
            data[entry.slug] = pokemon
        io.to_js(data, file_path)

    def to_csv(self, file_path) -> None:
        all_pokemon = []
        all_evolutions = []
        for entry in self:
            pokemon, evolutions = entry.to_dict()
            all_pokemon.append(pokemon)
            all_evolutions.extend(evolutions)
        pd.DataFrame(all_pokemon).to_csv(file_path / "pokemon.csv", index=False)
        pd.DataFrame(all_evolutions).to_csv(file_path / "evolutions.csv", index=False)

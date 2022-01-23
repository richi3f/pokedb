__all__ = ["PokemonDatabase"]

from collections.abc import Iterator
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

    def query(self, search_function: Callable[["Pokemon"], bool]) -> list["Pokemon"]:
        return [pokemon for pokemon in self._dict.values() if search_function(pokemon)]

    def __iter__(self) -> Iterator["Pokemon"]:
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

    def remove(self, i: Union["Pokemon", tuple[int, int], str]) -> None:
        if isinstance(i, tuple):
            index_to_remove = i
        elif isinstance(i, str):
            index_to_remove = self.get_by_slug(i).index
        elif i.__class__.__name__ == "Pokemon":
            index_to_remove = i.index
        else:
            raise ValueError("Input must be an ID, slug, or Pokémon.")
        removed_pokemon = self._dict.pop(index_to_remove)
        for pokemon in self:
            if removed_pokemon in pokemon.evolutions:
                pokemon._evolutions.remove(removed_pokemon)

    def to_js(self, file_path, **kwargs) -> None:
        data = {}
        for pokemon in self:
            entry = {
                "id": pokemon.base_id,
                "form_id": pokemon.form_id,
                "name": pokemon.name,
                "type": [*map(str, pokemon.pokemon_type)],
                "gender": [*map(str, pokemon.gender)],
                "gender_ratio": pokemon.gender_ratio,
                "gen": pokemon.generation,
                "egg": [*map(str, pokemon.egg_group)],
                "exp": str(pokemon.experience_group),
            }
            if pokemon.form_name:
                entry["form"] = pokemon.form_name
            if pokemon.color is not None:
                entry["color"] = str(pokemon.color)
            if pokemon.is_baby:
                entry["baby"] = True
            if pokemon.is_legendary:
                entry["legendary"] = True
            if pokemon.is_sublegendary:
                entry["sublegendary"] = True
            if pokemon.is_mythical:
                entry["mythical"] = True
            if pokemon.is_mega:
                entry["mega"] = True
            if pokemon.has_gigantamax:
                entry["gmax"] = True
            if pokemon.evolutions:
                entry["evolves"] = [evolution.index for evolution in pokemon.evolutions]
            data[pokemon.slug] = entry
        io.to_js(data, file_path, **kwargs)

    def to_csv(self, file_path) -> None:
        all_pokemon = []
        all_evolutions = []
        for entry in self:
            pokemon, evolutions = entry.to_dict()
            all_pokemon.append(pokemon)
            all_evolutions.extend(evolutions)
        pd.DataFrame(all_pokemon).to_csv(file_path / "pokemon.csv", index=False)
        pd.DataFrame(all_evolutions).to_csv(file_path / "evolutions.csv", index=False)

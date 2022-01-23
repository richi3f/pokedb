__all__ = ["Registrar"]

import csv
from typing import Callable, Union

from pokedb.core.enums import Color, EggGroup, ExperienceGroup, Gender, Type
from pokedb.core.singleton import Singleton
from pokedb.pokemon.database import PokemonDatabase
from pokedb.pokemon.pokemon import Pokemon

FIELD_FACTORIES = (
    ("base_id", int),
    ("form_id", int),
    ("slug", str),
    ("name", str),
    ("form_name", str),
    ("generation", int),
    ("gender_ratio", int),
    ("has_gigantamax", bool),
    ("is_baby", bool),
    ("is_mythical", bool),
    ("is_legendary", bool),
    ("is_sublegendary", bool),
    ("color", Color.from_str),
    ("experience_group", ExperienceGroup.from_str),
    ("pokemon_type", Type.from_str),
    ("gender", Gender.from_str),
    ("egg_group", EggGroup.from_str),
)


class _Registrar(metaclass=Singleton):
    def __init__(self) -> None:
        self.db = PokemonDatabase()

    def register(self, pokemon: Pokemon) -> None:
        self.db[pokemon.index] = pokemon

    def register_evolution(self, basic_form_index: tuple[int, int], evolution_index: tuple[int, int]) -> None:
        self.db[basic_form_index]._evolutions.append(self.db[evolution_index])

    def from_csv(self, pokemon_csv_path, evolutions_csv_path=None) -> None:
        with open(pokemon_csv_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.from_dict(row)
        if evolutions_csv_path is not None:
            with open(evolutions_csv_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row = {k: int(v) for k, v in row.items()}
                    index = row["base_id"], row["form_id"]
                    evolution_index = row["evolution_base_id"], row["evolution_form_id"]
                    self.register_evolution(index, evolution_index)

    def from_dict(self, data: dict) -> None:
        pokemon = Pokemon()
        field: str
        factory: Callable
        for field, factory in FIELD_FACTORIES:
            value: Union[tuple, None] = getattr(pokemon, field)
            if isinstance(value, tuple):
                # Field is dual value
                for i in range(2):
                    ith_field = f"{field}_{i}"
                    if data.get(ith_field):
                        setattr(pokemon, field, value + (factory(data[ith_field]),))
            elif data.get(field):
                # Field is single value
                setattr(pokemon, field, factory(data[field]))
        self.register(pokemon)

    def get_by_index(self, ids: list[tuple[int, int]]) -> tuple[Pokemon, ...]:
        return tuple(self.db[idx] for idx in ids)


Registrar = _Registrar()

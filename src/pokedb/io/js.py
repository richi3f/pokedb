__all__ = ["dump_database", "load_database", "read_js", "to_js"]

import json
import dataclasses
from typing import Any

from pokedb.core.enums import Color, EggGroup, ExperienceGroup, Gender, Type
from pokedb.core.typing import PathLike
from pokedb.pokemon.pokemon import Pokemon
from pokedb.pokemon.database import PokemonDatabase

JS_PREFIX = "export default "
JS_SUFFIX = ";"


def read_js(file_path: PathLike, **kwargs) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        file.seek(len(JS_PREFIX))
        json_str = file.read()[: -len(JS_SUFFIX)]
    return json.loads(json_str, **kwargs)


def deserialize_pokemon(dct: dict[str, Any]) -> Any:
    if "base_id" not in dct:
        return dct
    pokemon = Pokemon()
    for attr, value in dct.items():
        if attr == "color":
            value = Color[value]
        if attr == "egg_group":
            value = tuple(map(EggGroup.__getitem__, value))
        if attr == "experience_group":
            value = ExperienceGroup._value2member_map_[value]
        if attr == "gender":
            value = tuple(map(Gender._value2member_map_.__getitem__, value))
        if attr == "pokemon_type":
            value = tuple(map(Type.__getitem__, value))
        if attr == "evolution_ids":
            value = tuple(map(tuple, value))
        setattr(pokemon, attr, value)
    return pokemon


def load_database(file_path: PathLike) -> PokemonDatabase:
    database = PokemonDatabase()
    data = read_js(file_path, object_hook=deserialize_pokemon)
    for slug, pokemon in data.items():
        pokemon.slug = slug
        database[pokemon.index] = pokemon
    return database


def to_js(data: dict, file_path: PathLike, **kwargs) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(JS_PREFIX + json.dumps(data, **kwargs) + JS_SUFFIX)


class PokemonJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        for enum_type in [Color, EggGroup, Type]:
            if isinstance(o, enum_type):
                return o.name
        if isinstance(o, ExperienceGroup) or isinstance(o, Gender):
            return o.value
        return super().default(o)


def dump_database(database: PokemonDatabase, file_path: PathLike) -> None:
    database_asdict = {}
    for pokemon in database:
        pokemon_asdict = dataclasses.asdict(pokemon)
        pokemon_asdict.pop("slug")
        for key in list(pokemon_asdict.keys()):
            value = pokemon_asdict[key]
            is_false_or_empty = (
                isinstance(value, bool) or hasattr(value, "__len__")
            ) and not value
            if is_false_or_empty or pokemon_asdict[key] is None:
                pokemon_asdict.pop(key)
        database_asdict[pokemon.slug] = pokemon_asdict
    to_js(database_asdict, file_path, indent=4, cls=PokemonJSONEncoder)

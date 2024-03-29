__all__ = [
    "dump_database",
    "dump_pokedexes",
    "dump_versions",
    "load_database",
    "load_pokedexes",
    "load_versions",
    "read_js",
    "to_js",
]

import dataclasses
import json
import re
from typing import Any

from pokedb.core.enums import Color, EggGroup, ExperienceGroup, Gender, Type
from pokedb.core.typing import PathLike
from pokedb.games.pokedex import Pokedex
from pokedb.games.versions import VersionData
from pokedb.pokemon.database import PokemonDatabase
from pokedb.pokemon.pokemon import PastType, Pokemon

JS_PREFIX = "export default "
JS_SUFFIX = ";"


def read_js(file_path: PathLike, **kwargs) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        file.seek(len(JS_PREFIX))
        json_str = file.read()[: -len(JS_SUFFIX)]
    return json.loads(json_str, **kwargs)


def deserialize_pokemon(dct: dict[str, Any]) -> Any:
    def strtotype(value: str) -> Type:
        return Type[value.upper()]

    if "base_id" in dct and "form_id" in dct:
        pokemon = Pokemon()
        for attr, value in dct.items():
            if attr == "color":
                value = Color[str.upper(value)]
            elif attr == "egg_group":
                value = tuple(map(lambda x: EggGroup[str.upper(x)], value))
            elif attr == "experience_group":
                value = ExperienceGroup._value2member_map_[value]
            elif attr == "gender":
                value = tuple(map(Gender._value2member_map_.__getitem__, value))
            elif attr == "pokemon_type":
                value = tuple(map(strtotype, value))
            elif attr == "evolution_ids":
                value = tuple(map(tuple, value))
            elif attr == "past_type":
                pokemon_type = tuple(map(strtotype, value["pokemon_type"]))
                value = PastType(value["generation"], pokemon_type)
            setattr(pokemon, attr, value)
        return pokemon
    elif "name" in dct and "order" in dct:
        pokedex = Pokedex()
        for attr, value in dct.items():
            if attr == "order":
                dex_ids = map(int, value.keys())
                pokemon_ids = [[*map(tuple, x)] for x in value.values()]
                value = dict(zip(dex_ids, pokemon_ids))
            setattr(pokedex, attr, value)
        return pokedex
    return dct


def load_database(file_path: PathLike) -> PokemonDatabase:
    database = PokemonDatabase()
    data = read_js(file_path, object_hook=deserialize_pokemon)
    for slug, pokemon in data.items():
        pokemon.slug = slug
        database[pokemon.index] = pokemon
    return database


def load_pokedexes(file_path: PathLike) -> dict[str, Pokedex]:
    pokedexes: dict[str, Pokedex] = read_js(file_path, object_hook=deserialize_pokemon)
    for slug, pokedex in pokedexes.items():
        pokedex.slug = slug
    return pokedexes


def load_versions(file_path: PathLike) -> dict[str, VersionData]:
    dct = read_js(file_path)
    versions = {}
    for slug, value in dct.items():
        exclusives = sorted(map(tuple, value))
        versions[slug] = VersionData(slug, exclusives)
    return versions


def to_js(data: dict, file_path: PathLike, **kwargs) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(JS_PREFIX + json.dumps(data, **kwargs) + JS_SUFFIX)


class PokemonJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (Color, EggGroup, Type)):
            return o.name.lower()
        if isinstance(o, (ExperienceGroup, Gender)):
            return o.value
        return super().default(o)


def dump_database(database: PokemonDatabase, file_path: PathLike) -> None:
    database_asdict = {}
    for pokemon in database:
        pokemon_asdict = dataclasses.asdict(pokemon)
        pokemon_asdict.pop("slug")
        for key in list(pokemon_asdict.keys()):
            value = pokemon_asdict[key]
            is_bool_or_iter = isinstance(value, bool) or hasattr(value, "__len__")
            is_false_or_empty = is_bool_or_iter and not value
            if is_false_or_empty or pokemon_asdict[key] is None:
                pokemon_asdict.pop(key)
        database_asdict[pokemon.slug] = pokemon_asdict
    to_js(
        database_asdict, file_path, indent=4, ensure_ascii=False, cls=PokemonJSONEncoder
    )
    with open(file_path, "r+", encoding="utf-8") as file:
        file_contents = file.read()
        file_contents = re.sub(r"\n\s{16}", " ", file_contents)
        file_contents = re.sub(r"\n\s{12}\]", " ]", file_contents)
        file_contents = re.sub(r"\n\s{12}", " ", file_contents)
        file_contents = re.sub(r"\n\s{8}\]", " ]", file_contents)
        file_contents = re.sub(r"\n\s{8}\}", " }", file_contents)
        file.seek(0)
        file.write(file_contents)
        file.truncate()


def dump_pokedexes(pokedexes: dict[str, Pokedex], file_path: PathLike) -> None:
    pokedexes_asdict = {}
    for pokedex in pokedexes.values():
        pokedex_asdict = dataclasses.asdict(pokedex)
        pokedexes_asdict[pokedex_asdict.pop("slug")] = pokedex_asdict
    to_js(pokedexes_asdict, file_path, indent=4)
    with open(file_path, "r+", encoding="utf-8") as file:
        file_contents = file.read()
        file_contents = re.sub(r"\n\s{20}", " ", file_contents)
        file_contents = re.sub(r"\n\s{16}\]", " ]", file_contents)
        file_contents = re.sub(r"\n\s{16}", " ", file_contents)
        file_contents = re.sub(r"\n\s{12}\]", " ]", file_contents)
        file.seek(0)
        file.write(file_contents)
        file.truncate()


def dump_versions(versions: dict[str, VersionData], file_path: PathLike) -> None:
    versions_asdict = {}
    for version in versions.values():
        version_asdict = dataclasses.asdict(version)
        versions_asdict[version_asdict["slug"]] = version_asdict["exclusives"]
    to_js(versions_asdict, file_path, indent=4)
    with open(file_path, "r+", encoding="utf-8") as file:
        file_contents = file.read()
        file_contents = re.sub(r"\n\s{12}", " ", file_contents)
        file_contents = re.sub(r"\n\s{8}\]", " ]", file_contents)
        file.seek(0)
        file.write(file_contents)
        file.truncate()

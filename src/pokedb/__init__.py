__version__ = (0, 0, 0)
__all__ = ["core", "io", "Pokemon", "Pokedex", "PokemonDatabase", "VersionData"]

from pokedb import core, io
from pokedb.games.pokedex import Pokedex
from pokedb.games.versions import VersionData
from pokedb.pokemon.database import PokemonDatabase
from pokedb.pokemon.pokemon import Pokemon

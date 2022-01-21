from pokedb import __version__

from pokedb import PokemonDatabase, Pokemon


def test_version():
    assert __version__ == "0.0.0"


def test_create_pokemon():
    # Pokémon should be created and added to the database
    sableye = Pokemon(302, 0)
    assert PokemonDatabase[302] == sableye

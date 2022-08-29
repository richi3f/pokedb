:card_file_box: pokedb
======================

A Pokémon database

## Installation

Change directory to root of the package, and then:

```
pip install -e .
```

## Examples

Load the database:

```python
>>> import pokedb
>>> database = pokedb.io.load_database("data/pokemon.js")
>>> database[302]
Sableye
```

Fetch information:

```python
>>> database["enamorus"].pokemon_type
(<Type.FAIRY: 18>, <Type.FLYING: 3>)
```


Query the database:

```python
>>> database.query(lambda pokemon: pokemon.name.startswith("Regi"))
[Regirock, Regice, Registeel, Regigigas, Regieleki, Regidrago]
```

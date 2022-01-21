from dataclasses import dataclass, field

import pokedb


@dataclass
class Pokemon:
    base_id: int
    form_id: int
    name: str = None
    form_name: str = None
    genders: list = field(default_factory=list)
    types: list = field(default_factory=list)
    is_gigantamax: bool = False
    is_sublegendary: bool = False
    is_legendary: bool = False
    is_mythical: bool = False
    is_baby: bool = False

    def __post_init__(self):
        pokedb.PokemonDatabase[(self.base_id, self.form_id)] = self

    @property
    def slug(self):
        return self.name.lower()

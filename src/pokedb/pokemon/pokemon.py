__all__ = ["Pokemon"]

import dataclasses
from functools import total_ordering
from dataclasses import dataclass
from typing import Optional, Union

from pokedb.core.enums import Color, ExperienceGroup, Gender, Type
from pokedb.core.typing import (
    PokemonBaseAndFormIndex,
    PokemonEggGroup,
    PokemonType,
    SingleOrDualType,
)
from pokedb.pokemon.html_repr import pokemon_html


@dataclass
class PastType:
    generation: Optional[int] = None
    pokemon_type: PokemonType = ()


@dataclass
@total_ordering
class Pokemon:
    base_id: Optional[int] = None
    form_id: Optional[int] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    form_name: Optional[str] = None
    pokemon_type: PokemonType = ()
    past_type: Optional[PastType] = None
    egg_group: PokemonEggGroup = ()
    gender: tuple[Gender, ...] = ()
    gender_ratio: Optional[int] = None
    has_gigantamax: bool = False
    is_sublegendary: bool = False
    is_legendary: bool = False
    is_mythical: bool = False
    is_baby: bool = False
    is_mega: bool = False
    is_cosmetic: bool = False
    is_battle_only: bool = False
    color: Optional[Color] = None
    experience_group: Optional[ExperienceGroup] = None
    generation: Optional[int] = None
    evolution_ids: tuple[PokemonBaseAndFormIndex, ...] = ()

    @property
    def index(self) -> tuple[int, int]:
        assert self.base_id is not None
        assert self.form_id is not None
        return self.base_id, self.form_id

    def set_past_type(
        self, generation: int, pokemon_type: Union[Type, SingleOrDualType]
    ) -> None:
        if isinstance(pokemon_type, Type):
            pokemon_type = (pokemon_type,)
        self.past_type = PastType(generation, pokemon_type)

    def __eq__(self, other: "Pokemon") -> bool:
        return self.index == other.index

    def __lt__(self, other: "Pokemon") -> bool:
        return self.index < other.index

    def __repr__(self) -> str:
        suffix = "" if not self.form_name else f" ({self.form_name})"
        return f"{self.name}{suffix}"

    def _repr_html_(self) -> str:
        return pokemon_html(self)

    def new(self, **kwargs) -> "Pokemon":
        """Creates a new Pokémon by copying the data from another one. Values
        can be overriden by supplying keyword arguments.

        Returns:
            A new Pokémon instance
        """
        old_instance = dataclasses.asdict(self)
        new_instance = Pokemon()
        for field in old_instance.keys():
            value = old_instance[field] if field not in kwargs else kwargs[field]
            setattr(new_instance, field, value)
        return new_instance

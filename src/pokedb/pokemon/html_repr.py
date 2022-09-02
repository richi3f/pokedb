__all__ = ["pokemon_html"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pokedb.pokemon.pokemon import Pokemon


def pokemon_html(pokemon: "Pokemon"):
    gender_ratio = pokemon.gender_ratio / 8
    if gender_ratio < 0:
        gender_ratio = "Gender unkown"
    elif gender_ratio == 0:
        gender_ratio = "100% male"
    elif gender_ratio == 1:
        gender_ratio = "100% female"
    else:
        gender_ratio = f"{1 - gender_ratio:.0%} male, {gender_ratio:.0%} female"
    table = f"""
    <table>
        <tr>
            <th colspan="2">{pokemon.__repr__()}</th>
        </tr>
        <tr>
            <th>Generation</th>
            <td>{pokemon.generation}</td>
        </tr>
        <tr>
            <th>Type</th>
            <td>{" / ".join(map(lambda t: t.name, pokemon.pokemon_type))}</td>
            </tr>"""
    if pokemon.past_type:
        table += f"""
        <tr>
            <th>Past Type</th>
            <td>{" / ".join(map(lambda t: t.name, pokemon.past_type.pokemon_type))}<br>
            (prior to Generation {pokemon.past_type.generation})</td>
        </tr>"""
    table += f"""
        <tr>
            <th>Gender Ratio</th>
            <th>{gender_ratio}</th>
        </tr>
        <tr>
            <th>Egg Group</th>
            <th>{" / ".join(map(lambda g: g.name, pokemon.egg_group))}</th>
        </tr>
        <tr>
            <th>Color</th>
            <th>{pokemon.color.name}</th>
        </tr>
        <tr>
            <th>Experience Group</th>
            <th>{pokemon.experience_group.name}</th>
        </tr>
        """
    tags = []
    if pokemon.is_mega:
        tags.append("Mega")
    if pokemon.is_baby:
        tags.append("Baby")
    if pokemon.is_sublegendary:
        tags.append("Sub-Legendary")
    if pokemon.is_legendary:
        tags.append("Legendary")
    if pokemon.is_mythical:
        tags.append("Mythical")
    if pokemon.has_gigantamax:
        tags.append("Has Gigantamax Form")
    if tags:
        table += f"""
        <tr>
            <th>Tag</th>
            <td>{", ".join(tags)}</td>
        </tr>
    """
    table += "</table>"
    return table
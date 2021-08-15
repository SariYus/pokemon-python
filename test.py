from client import add_pokemon, get_pokemons_by_type, update_pokemon_types, get_pokemons_by_owner, \
    get_owners_of_a_pokemon, evolve


def test_get_pokemons_by_type():
    assert "eevee" in get_pokemons_by_type("normal")


def test_add_pokemon():
    add_pokemon("yanma")
    assert "yanma" in get_pokemons_by_type("bug")
    assert "yanma" in get_pokemons_by_type("flying")
    assert add_pokemon("yanma") == 503


def test_update_pokemon_type():
    assert update_pokemon_types("venusaur") == 200
    assert "venusaur" in get_pokemons_by_type("poison")
    assert "venusaur" in get_pokemons_by_type("grass")


def test_get_pokemons_by_owner():
    assert get_pokemons_by_owner("Drasna") == ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff",
                                               "persian", "growlithe", "machamp", "golem", "dodrio", "hypno", "cubone",
                                               "eevee", "kabutops"]


def test_get_owners_of_a_pokemon():
    assert get_owners_of_a_pokemon("charmander") == ["Giovanni", "Jasmine", "Whitney"]


def test_evolve():
    assert evolve("pinsir", "Whitney").status_code == 503
    assert evolve("oddish", "Whitney").status_code == 200

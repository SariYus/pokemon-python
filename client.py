
import requests

from config import url_server
from poke_api_module import get_pokemon_data


def add_pokemon(pokemon_name):
    pokemon_details = get_pokemon_data(pokemon_name)
    res = requests.post(url_server + f"/add_pokemon/{pokemon_details.get('id')}", json={"id": pokemon_details.get('id'), "name": pokemon_details.get('name'),
                                    "height": pokemon_details.get('height'),
                                    "weight": pokemon_details.get('weight'), "types": pokemon_details.get('types')})
    return res.status_code


def get_pokemons_by_type(typ):
    res = requests.get(url_server + f"/get_pokemon_by_type/{typ}")
    return res.json()


def update_pokemon_types(pokemon_name):
    res = requests.put(url_server + f"/update_type/{pokemon_name}")
    return res.status_code


def get_pokemons_by_owner(trainer):
    res = requests.get(url_server + f"/get_pokemons?trainer_name={trainer}")
    return res.json()


def get_owners_of_a_pokemon(pokemon_name):
    res = requests.get(url_server + f"/get_trainers?pokemon_name={pokemon_name}")
    return res.json()


def evolve(pokemon_name, trainer):
    res = requests.post(url_server + f"/evolve/{pokemon_name}/{trainer}")
    return res

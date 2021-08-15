import requests

from config import url_pokemon_api


def get_pokemon_data(pokemon_name):
    pokemon_url = url_pokemon_api + f'{pokemon_name}/'
    res = requests.get(pokemon_url, verify=False).json()
    return res

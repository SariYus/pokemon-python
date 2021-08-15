import json

import requests

from flask import Flask, request, Response

from config import port
from db_module_sql import insert_types, insert_pokemon, insert_type, find_by_type, get_pokemon, find_roster, \
    find_owners, \
    delete_pokemon_from_owns, update_owns, load_data
from poke_api_module import get_pokemon_data

app = Flask(__name__)


@app.route("/update_type/<pokemon_name>", methods=["PUT"])
def update_type(pokemon_name):
    """
    Update types in database according to a pokemon's types
    :param pokemon_name: pokemon to update by it
    :return: success (status 200) if success, error message (status 501) otherwise.
    """
    try:
        pokemon_details = get_pokemon_data(pokemon_name)
        list(map(lambda type_obj: insert_types(type_obj, pokemon_details["id"]), pokemon_details['types']))
        return Response("success")
    except:
        return Response(f"cannot update type for {pokemon_name}", 501)


@app.route("/add_pokemon/<pokemon_id>", methods=['POST'])
def add_pokemon(pokemon_id):
    """
    Get id, name, height and weight, and add a new pokemon to database
    :param pokemon_id: required parameter to insert pokemon
    :return: success (status 200) if success, error message (status 501) otherwise.
    """
    try:
        req = request.get_json()
        err = insert_pokemon({"id": pokemon_id, "name": req.get('name'), "height": req.get('height'),
                              "weight": req.get('weight')})
        if err == "exist pokemon":
            return Response(err, 503)
        list(map(lambda type_obj: insert_types(type_obj, pokemon_id), req.get('types')))
        return Response("success")
    except:
        return Response(f"cannot add pokemon {pokemon_id}", 501)


@app.route("/get_pokemon_by_type/<typ>", methods=['GET'])
def get_pokemon_by_type(typ):
    """
    Find all pokemons with the mentioned type
    :param typ: type to search in database
    :return: suitable pokemons (status 200) if success, error message (status 501) otherwise.
    """
    try:
        return Response(json.dumps(find_by_type(typ)))
    except:
        return Response(f"cannot find pokemons", 501)


@app.route("/evolve/<pokemon_name>/<trainer>", methods=['POST'])
def evolve(pokemon_name, trainer):
    """
    Evolve a trainer's pokemon according to evolution chain
    :param pokemon_name: pokemon needs to evolve
    :param trainer: trainer owns the pokemon needs to evolve
    :return: success (status 200) if evolved, end message (status 503) if chain ended, and error message (status 501) if failed.
    """
    try:
        pokemon_id = get_pokemon(pokemon_name)
        pokemon = get_pokemon_data(pokemon_name)
        species = requests.get(pokemon['species']['url'], verify=False).json()
        evolution_chain = requests.get(species['evolution_chain']['url'], verify=False).json()
        chain = [evolution_chain['chain']]
        while chain[0]['species']['name'] != pokemon_name:
            chain = chain[0]['evolves_to']
        if not chain[0]['evolves_to']:
            return Response("you got the end of pokemon evolving", 503)
        new_pokemon = chain[0]['evolves_to'][0]['species']['name']
        update_owns(pokemon['id'], trainer, new_pokemon)
        return Response('success')
    except:
        return Response(f"pokemon {pokemon_name} of trainer {trainer} cannot evolve", 501)
    return Response('successes')


@app.route("/get_pokemons", methods=["GET"])
def get_pokemons():
    """
    Get a trainer name and find his pokemons
    :return: pokemons list (status 200) if success, error message (status 501) otherwise.
    """
    try:
        trainer = request.args.get("trainer_name")
        return Response(json.dumps(find_roster(trainer)))
    except Exception:
        return Response(f"cannot find pokemons for {trainer}", 501)


@app.route("/get_trainers", methods=["GET"])
def get_trainers():
    """
    Get a pokemon name and find it's owners
    :return: trainers list (status 200) if success, error message (status 501) otherwise.
    """
    try:
        pokemon = request.args.get("pokemon_name")
        return Response(json.dumps(find_owners(pokemon)))
    except:
        return Response(f"cannot find trainers for {pokemon}", 501)


@app.route("/delete_pokemon/<pokemon_id>", methods=["DELETE"])
def delete_pokemon(pokemon_id):
    """
    Delete a pokemon and trainer ownership
    :param pokemon_id: id of pokemon needs to be deleted
    :return: success message (status 200) if success, and error message (status 501) otherwise.
    """
    try:
        delete_pokemon_from_owns(pokemon_id)
        return Response(f"pokemon {pokemon_id} deleted successfully from database")
    except Exception:
        return Response(f"cannot delete pokemon {pokemon_id}", 501)


if __name__ == '__main__':
    app.run(port=port)


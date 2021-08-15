import json

import pymysql

from config import connection


def insert_trainer(own):
    """
    Insert a new trainer to database
    :param own: new trainer details
    """
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO trainer VALUES (%s, %s)"
            cursor.execute(query, (own['name'], own['town']))
            connection.commit()
    except pymysql.err.IntegrityError:
        pass
    except Exception as e:
        print("insert_trainer:", e)


def insert_owns(id, name):
    """
    Insert a new pokemon and trainer ownership to database
    :param id: pokemon id
    :param name: trainer name
    """
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO owns VALUES (%s, %s)"
            cursor.execute(query, (id, name))
            connection.commit()
    except Exception as e:
        print("insert_owns:", e)


def insert_pokemon(pokemon):
    """
    Insert a new pokemon to database
    :param pokemon: pokemon details
    """
    if connection.open:
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO pokemon VALUES (%s, %s, %s, %s)"
                cursor.execute(query,
                               (pokemon['id'], pokemon['name'], pokemon['height'], pokemon['weight']))
                connection.commit()
        except pymysql.err.IntegrityError:
            return "exist pokemon"
        except Exception as e:
            print("insert_pokemon:", e)


def insert_trainer_and_own(trainer, pokemon_id):
    """
    Insert new trainer and his ownership to database
    :param trainer: trainer name to insert by it
    :param pokemon_id: pokemon id to insert by it
    """
    insert_trainer(trainer)
    insert_owns(pokemon_id, trainer['name'])


def insert_data(obj):
    """
    Insert pokemon, it's types and it's ownership
    :param obj: obj represents the pokemon data
    """
    insert_pokemon(obj)
    insert_types({"type": {"name": obj['type']}}, obj['id'])
    list(map(lambda own: insert_trainer_and_own(own, obj['id']), obj['ownedBy']))


def load_data():
    """
    Load data from json file to database
    """
    with open("pokemon_data.json", "r") as pokemon_file:
        data = json.load(pokemon_file)
        list(map(insert_data, data))


def find_roster(trainer_name):
    """
    Find all pokemons of a trainer
    :param trainer_name: trainer name to search in database
    :return: pokemons' names list
    """
    with connection.cursor() as cursor:
        query = "SELECT DISTINCT name FROM owns, pokemon " \
                f"WHERE trainer_name = '{trainer_name}' and id = pokemon_id"
        cursor.execute(query)
        result = cursor.fetchall()
        return list(map(lambda obj: obj['name'], result))


def find_owners(pokemon_name):
    """
    Find all owners of a pokemon
    :param pokemon_name: pokemon name to search in database
    :return: owners' list
    """
    with connection.cursor() as cursor:
        query = "SELECT Trainer.name FROM Trainer JOIN Owns JOIN Pokemon " \
                "ON Trainer.name = trainer_name AND " \
                "id = pokemon_id " \
                f"WHERE Pokemon.name = '{pokemon_name}'"
        cursor.execute(query)
        result = cursor.fetchall()
        return list(map(lambda obj: obj['name'], result))


def finds_most_owned():
    """
    Find pokemon/s with the most owners
    :return: found pokemons' list
    """
    with connection.cursor() as cursor1:
        query = "SELECT name FROM owns, pokemon where owns.pokemon_id = pokemon.id GROUP BY " \
                "pokemon_id having count(*) >=ALL(select count(*) FROM owns GROUP BY pokemon_id)"
        cursor1.execute(query)
        return list(map(lambda obj: obj['name'], cursor1.fetchall()))


def heaviest_pokemon():
    """
    Find pokemon/s with the ighest weight
    :return: found pokemons' list
    """
    with connection.cursor() as cursor:
        query = "SELECT name FROM Pokemon WHERE weight IN" \
                "(SELECT MAX(weight) FROM Pokemon)"
        cursor.execute(query)
        result = cursor.fetchall()
        return list(map(lambda obj: obj['name'], result))


def find_by_type(typ):
    """
    Find pokemons have the given type
    :param typ: type to search
    :return: found pokemons' list
    """
    with connection.cursor() as cursor:
        query = "SELECT DISTINCT Pokemon.name FROM Pokemon, pokemon_type " \
                f"WHERE pokemon_type.typ = '{typ}' and Pokemon.id = pokemon_type.pokemon_id"
        cursor.execute(query)
        result = cursor.fetchall()
        return list(map(lambda obj: obj['name'], result))


def insert_type(type_obj):
    """
    Insert new type to database
    :param type_obj: object with type details
    """
    try:
        with connection.cursor() as cursor:
            query = "insert into types values (%s)"
            cursor.execute(query, (type_obj['name']))
            connection.commit()
    except pymysql.err.IntegrityError:
        pass
    except Exception as e:
        print("insert_type:", e)


def insert_pokemon_type(type_name, pokemon_id, slot):
    """
    Insert data about a type of a pokemon
    :param type_name: type name to insert
    :param pokemon_id: pokemon id to insert
    :param slot: info about the type
    """
    try:
        with connection.cursor() as cursor:
            query = "insert into pokemon_type values (%s, %s)"
            cursor.execute(query, (pokemon_id, type_name))
            connection.commit()
    except Exception as e:
        print("insert_pokemon_type:", e)


def insert_types(type_obj, pokemon_id):
    """
    Insert pokemon's type to database by calling the functions above.
    :param type_obj: type object to insert
    :param pokemon_id: pokemon id to insert
    """
    insert_type(type_obj['type'])
    insert_pokemon_type(type_obj['type']['name'], pokemon_id, type_obj.get('slot'))


def get_pokemon(pokemon_name):
    """
    Find pokemon's id by pokemon's name
    :param pokemon_name: pokemon name to search
    :return: pokemon's id
    """
    try:
        with connection.cursor() as cursor:
            query = f"select id from pokemon where name = {pokemon_name}"
            cursor.execute(query)
            return cursor.fetchone()['id']
    except Exception as e:
        print("get_pokemon:", e)


def delete_pokemon_from_owns(id):
    """
    Delete from database a pokemon's ownership
    :param id: pokemon id to search and delete
    """
    with connection.cursor() as cursor:
        query = "DELETE FROM Owns " \
                f"WHERE pokemon_id = {id}"
        cursor.execute(query)
        connection.commit()


def update_owns(old_pokemon_id, trainer_name, new_pokemon_name):
    """
    Update an owner has a pokemon in database to have a new pokemon
    :param old_pokemon_id: id of the previous pokemon, has to evolve
    :param trainer_name: name of trainer have to be updated
    :param new_pokemon_name: new pokemon to put in the ownership
    """
    with connection.cursor() as cursor:
        query = "UPDATE Owns " \
                "SET pokemon_id = (" \
                "SELECT id FROM Pokemon " \
                f"WHERE name = '{new_pokemon_name}') " \
                f"WHERE pokemon_id = {old_pokemon_id} AND " \
                f"trainer_name = '{trainer_name}'"
        print(query)
        cursor.execute(query)
        connection.commit()

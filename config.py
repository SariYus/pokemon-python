import pymysql

port = 5000
url_pokemon_api = "https://pokeapi.co/api/v2/pokemon/"
url_server = 'http://localhost:' + str(port)

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="sari230801",
    db="sql_intro",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
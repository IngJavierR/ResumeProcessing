import os
import psycopg2
from langchain_community.utilities import SQLDatabase



def setup_database(catalog):
    DB_USER, DB_PASS, DB_PORT, IP_DB, DATABASE_NAME = database_origin(catalog)
    # Setup database
    return SQLDatabase.from_uri(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{IP_DB}:{DB_PORT}/{DATABASE_NAME}",
    )

def insert_db(catalog, sentence):
    DB_USER, DB_PASS, DB_PORT, IP_DB, DATABASE_NAME = database_origin(catalog)
    conn = None
    cur = None
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=IP_DB,
            port=DB_PORT
        )

        # Crear un cursor
        cur = conn.cursor()
        # Execute sentence
        cur.execute(sentence)
        # Cerrar comunicación con la base de datos
        conn.commit()
    except Exception as e:
        print('Sentence', sentence)
        print('Error al insertar', e)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


def database_origin(catalog):
    DB_USER = ''
    DB_PASS = ''
    DB_PORT = ''
    IP_DB = ''
    DATABASE_NAME = ''

    if catalog == 'people':
        DB_USER = os.environ.get('DBUSER')
        DB_PASS = os.environ.get('DBPASS')
        DB_PORT = os.environ.get('DBPORT')
        IP_DB = os.environ.get('IPDB')
        DATABASE_NAME = os.environ.get('DATABASE')

    return DB_USER, DB_PASS, DB_PORT, IP_DB, DATABASE_NAME
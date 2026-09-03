import psycopg

from pgvector.psycopg import register_vector

from config import DATABASE_URL


def get_connection():

    connection = psycopg.connect(
        DATABASE_URL
    )

    register_vector(connection)
    return connection

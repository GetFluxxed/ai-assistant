import psycopg

from config import DATABASE_URL


def main():

    with psycopg.connect(
        DATABASE_URL,
        autocommit=True
    ) as conn:

        conn.execute(
            """
            CREATE EXTENSION IF NOT EXISTS vector;
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS document_chunks (
                id BIGSERIAL PRIMARY KEY,
                source_name TEXT NOT NULL,
                page_number INTEGER,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                embedding VECTOR(1536) NOT NULL
            );
            """
        )

    print("Database initialized successfully.")


if __name__ == "__main__":
    main()
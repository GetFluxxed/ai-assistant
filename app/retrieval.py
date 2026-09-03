from pgvector import Vector

from db import get_connection
from embeddings import create_embedding

#Retrieves chunks for similar comparison using Semantic Search via Vector

def retrieve_chunks(
    question: str,
    limit: int = 5
):

    question_embedding = create_embedding(
        question
    )

    vector = Vector(
        question_embedding
    )

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    source_name,
                    page_number,
                    chunk_index,
                    content,
                    1 - (embedding <=> %s) AS similarity

                FROM document_chunks

                ORDER BY embedding <=> %s

                LIMIT %s
                """,

                (
                    vector,
                    vector,
                    limit
                )
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "source_name": row[1],
            "page_number": row[2],
            "chunk_index": row[3],
            "content": row[4],
            "similarity": float(row[5])
        }

        for row in rows
    ]
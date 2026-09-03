from openai import OpenAI

from config import EMBEDDING_MODEL


client = OpenAI()


def create_embeddings(
    texts: list[str]
) -> list[list[float]]:

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [
        item.embedding
        for item in response.data
    ]


def create_embedding(
    text: str
) -> list[float]:

    return create_embeddings([text])[0]

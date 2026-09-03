from openai import OpenAI

from config import EMBEDDING_MODEL


client = OpenAI()

# Function creates Embeds to be stored within database which can be called later

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

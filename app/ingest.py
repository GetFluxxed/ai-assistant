from pathlib import Path
from embeddings import create_embeddings
from pgvector import Vector

from db import get_connection

import fitz


DOCUMENT_FOLDER = Path("documents")


def extract_pdf(path: Path):

    document = fitz.open(path)

    pages = []

    for page_number, page in enumerate(
        document,
        start=1
    ):

        text = page.get_text("text")

        if text.strip():

            pages.append({
                "page_number": page_number,
                "text": text
            })

    return pages

def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 80
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks

def process_pdf(path: Path):

    pages = extract_pdf(path)

    processed_chunks = []

    for page in pages:

        page_chunks = chunk_text(
            page["text"]
        )

        for index, content in enumerate(
            page_chunks
        ):

            processed_chunks.append({
                "source_name": path.name,
                "page_number": page["page_number"],
                "chunk_index": index,
                "content": content
            })


    return processed_chunks
def embed_chunks(chunks):

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = create_embeddings(texts)

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        chunk["embedding"] = embedding

    return chunks
def save_chunks(chunks):
    if not chunks:
        raise ValueError("No chunks to save")

    source_name = chunks[0]["source_name"]

    if any(chunk["source_name"] != source_name for chunk in chunks):
        raise ValueError("Save one document at a time")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Remove the previous version of this document.
            cursor.execute(
                """
                DELETE FROM document_chunks
                WHERE source_name = %s
                """,
                (source_name,)
            )

            # Insert its complete, freshly processed chunks.
            for chunk in chunks:
                cursor.execute(
                    """
                    INSERT INTO document_chunks
                    (
                        source_name,
                        page_number,
                        chunk_index,
                        content,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        chunk["source_name"],
                        chunk["page_number"],
                        chunk["chunk_index"],
                        chunk["content"],
                        Vector(chunk["embedding"])
                    )
                )

        conn.commit()

def ingest_document(path: Path):

    print(f"Processing {path.name}")

    chunks = process_pdf(path)

    print(
        f"Created {len(chunks)} chunks"
    )

    chunks = embed_chunks(chunks)

    print("Created embeddings")

    save_chunks(chunks)

    print("Saved to database")


def ingest_all_documents():

    for path in DOCUMENT_FOLDER.glob("*.pdf"):

        ingest_document(path)


if __name__ == "__main__":

    ingest_all_documents()
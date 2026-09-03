from pathlib import Path
from embeddings import create_embeddings
from pgvector import Vector

from db import get_connection

import fitz


DOCUMENT_FOLDER = Path("documents")

# Function iterates through pages storing data as text and parsing page number and contents.

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

# This function defines how big our chunks are going to be, and the form we store them in

def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 80
):

# This iterates through all of our words within our chunk and appends them together in a list 

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

# This is parsing the information out of the chunks that we stored previously 

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

# This turns the chunks contents into embeds that will be stored as 1536 numbers in the database

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

# This saves the chunks and their embeds to the database

def save_chunks(chunks):
    if not chunks:
        raise ValueError("No chunks to save")

    source_name = chunks[0]["source_name"]

    if any(chunk["source_name"] != source_name for chunk in chunks):
        raise ValueError("Save one document at a time")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Remove the previous version of the document if redundant
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

    #Entire workflow of scraping the PDF's and storing to the database

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


# Ingests documents 1 by 1

def ingest_all_documents():

    for path in DOCUMENT_FOLDER.glob("*.pdf"):

        ingest_document(path)


if __name__ == "__main__":

    ingest_all_documents()
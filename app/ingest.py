from pathlib import Path

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
import re


def clean_text(text: str) -> str:
    """
    Clean extracted legal document text.
    """

    # Replace multiple spaces with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at beginning/end of lines
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150
):
    """
    Divide legal document into overlapping chunks.

    chunk_size:
        Approximate number of words per chunk.

    overlap:
        Number of words repeated between chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

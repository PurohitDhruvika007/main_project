from pathlib import Path

from app.services.text_extractor import extract_text
from app.services.text_chunker import clean_text, chunk_text


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


def validate_file(filename: str):

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. "
            "Only PDF, DOCX and TXT files are allowed."
        )

    return extension


def process_document(file_path: str):

    # Extract text
    text = extract_text(file_path)

    # Clean text
    cleaned_text = clean_text(text)

    # Create chunks
    chunks = chunk_text(
        cleaned_text,
        chunk_size=800,
        overlap=150
    )

    return {
        "text": cleaned_text,
        "chunks": chunks,
        "character_count": len(cleaned_text),
        "word_count": len(cleaned_text.split()),
        "chunk_count": len(chunks)
    }

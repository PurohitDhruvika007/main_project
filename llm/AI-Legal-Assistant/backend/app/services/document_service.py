from pathlib import Path

from app.services.text_extractor import extract_text
from app.services.text_chunker import clean_text, chunk_text


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}

MIN_TEXT_LENGTH = 50
MAX_FILE_SIZE = 20 * 1024 * 1024


def validate_file(filename: str):
    if not filename or not filename.strip():
        raise ValueError(
            "No file selected."
        )

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. "
            "Only PDF, DOCX and TXT files are allowed."
        )

    return extension


def validate_file_size(file_size: int):
    if file_size <= 0:
        raise ValueError(
            "The uploaded file is empty. "
            "Please upload a document containing legal content."
        )

    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            "File is too large. "
            "Maximum allowed file size is 20 MB."
        )


def process_document(file_path: str):

    path = Path(file_path)

    if not path.exists():
        raise ValueError(
            "Uploaded document could not be found."
        )

    file_size = path.stat().st_size

    validate_file_size(file_size)

    try:
        text = extract_text(str(path))

    except Exception as e:
        raise ValueError(
            "The uploaded document could not be read. "
            "The file may be corrupted or invalid."
        ) from e

    if not text or not text.strip():
        raise ValueError(
            "No readable text was found in the document. "
            "Please upload a document containing selectable text."
        )

    cleaned_text = clean_text(text)

    if not cleaned_text or not cleaned_text.strip():
        raise ValueError(
            "The document does not contain usable text."
        )

    if len(cleaned_text.strip()) < MIN_TEXT_LENGTH:
        raise ValueError(
            "The document contains too little readable content "
            "to perform legal analysis."
        )

    chunks = chunk_text(
        cleaned_text,
        chunk_size=800,
        overlap=150
    )

    if not chunks:
        raise ValueError(
            "The document could not be divided into usable text sections."
        )

    return {
        "text": cleaned_text,
        "chunks": chunks,
        "character_count": len(cleaned_text),
        "word_count": len(cleaned_text.split()),
        "chunk_count": len(chunks)
    }

from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""

    reader = PdfReader(file_path)

    text = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            text.append(f"\n--- Page {page_number} ---\n")
            text.append(page_text)

    return "\n".join(text)


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a TXT file."""

    path = Path(file_path)

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def extract_text(file_path: str) -> str:
    """Automatically extract text based on file extension."""

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

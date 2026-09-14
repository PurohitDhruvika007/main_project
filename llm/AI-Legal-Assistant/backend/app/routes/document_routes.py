from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_service import (
    validate_file,
    process_document
)

from app.services.embedding_service import generate_embeddings
from app.services.vector_store import create_vector_store
from app.services.simplification_service import simplify_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


CURRENT_DOCUMENT_FILE = UPLOAD_DIR / "current_document.txt"


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file or not file.filename:
        raise HTTPException(
            status_code=400,
            detail=(
                "No file selected. "
                "Please upload a PDF, DOCX or TXT file."
            )
        )

    file_path = None

    try:

        # Validate file extension
        extension = validate_file(
            file.filename
        )

        # Keep original filename
        original_name = Path(
            file.filename
        ).name

        # Create unique filename
        document_id = uuid.uuid4().hex

        unique_name = (
            f"{document_id}_{original_name}"
        )

        file_path = UPLOAD_DIR / unique_name

        # Save uploaded file
        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # Check file size
        file_size = file_path.stat().st_size

        if file_size == 0:
            raise ValueError(
                "The uploaded file is empty. "
                "Please upload a valid legal document."
            )

        # Extract, clean and chunk document
        result = process_document(
            str(file_path)
        )

        chunks = result["chunks"]

        if not chunks:
            raise ValueError(
                "No usable content was found in the document."
            )

        # Generate embeddings
        embeddings = generate_embeddings(
            chunks
        )

        # Create document-specific vector store
        vector_result = create_vector_store(
            embeddings=embeddings,
            texts=chunks,
            document_id=document_id,
            filename=original_name
        )

        # Store current document information
        with open(
            CURRENT_DOCUMENT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                f"{document_id}\n"
                f"{original_name}\n"
                f"{unique_name}"
            )

        return {
            "message": (
                "Document uploaded, processed "
                "and indexed successfully."
            ),
            "document_id": document_id,
            "filename": original_name,
            "file_type": extension,
            "file_size": file_size,
            "character_count": result["character_count"],
            "word_count": result["word_count"],
            "chunk_count": result["chunk_count"],
            "embedding_dimension": vector_result["dimension"],
            "total_vectors": vector_result["total_vectors"],
            "text_preview": result["text"][:1000],
            "first_chunk": chunks[0] if chunks else ""
        }

    except ValueError as e:

        # Delete invalid uploaded file
        if file_path and file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        # Delete file if processing fails
        if file_path and file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "Document processing failed. "
                f"{str(e)}"
            )
        )

    finally:
        file.close()


@router.post("/summary")
async def summarize_document():

    try:

        if not CURRENT_DOCUMENT_FILE.exists():
            raise HTTPException(
                status_code=404,
                detail=(
                    "No document has been uploaded yet."
                )
            )

        # Read current document information
        with open(
            CURRENT_DOCUMENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.read().splitlines()

        if len(lines) < 3:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Current document information is invalid."
                )
            )

        document_id = lines[0]
        original_name = lines[1]
        unique_name = lines[2]

        file_path = UPLOAD_DIR / unique_name

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=(
                    "The current uploaded document "
                    "could not be found."
                )
            )

        # Process current document
        result = process_document(
            str(file_path)
        )

        # Generate summary
        summary = simplify_document(
            result["text"]
        )

        return {
            "document_id": document_id,
            "filename": original_name,
            "summary": summary
        }

    except HTTPException:
        raise

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Document summarization failed. "
                f"{str(e)}"
            )
        )

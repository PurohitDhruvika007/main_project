from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_service import (
    validate_file,
    process_document
)

from app.services.embedding_service import generate_embeddings

from app.services.vector_store import create_vector_store


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    try:
        # Validate extension
        extension = validate_file(file.filename)

        # Create safe filename
        safe_filename = Path(file.filename).name

        file_path = UPLOAD_DIR / safe_filename

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get file size
        file_size = file_path.stat().st_size

        # Extract, clean and chunk document
        result = process_document(str(file_path))

        chunks = result["chunks"]

        # Generate embeddings for all chunks
        embeddings = generate_embeddings(chunks)

        # Store embeddings and chunks in FAISS
        vector_result = create_vector_store(
            embeddings,
            chunks
        )

        return {
            "message": "Document uploaded, processed and indexed successfully.",
            "filename": safe_filename,
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

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )


from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.services.vector_store import load_vector_store
from app.services.recommendation_service import generate_recommendations


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


UPLOAD_DIR = Path("uploads")
CURRENT_DOCUMENT_FILE = UPLOAD_DIR / "current_document.txt"


def get_current_document_id():

    if not CURRENT_DOCUMENT_FILE.exists():
        return None

    try:

        with open(
            CURRENT_DOCUMENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.read().splitlines()

        if not lines:
            return None

        document_id = lines[0].strip()

        if not document_id:
            return None

        return document_id

    except Exception:
        return None


@router.get("/analyze")
async def analyze_document_recommendations():

    document_id = get_current_document_id()

    if not document_id:

        raise HTTPException(
            status_code=404,
            detail=(
                "No document has been uploaded yet. "
                "Please upload a legal document first."
            )
        )

    try:

        index, records = load_vector_store()

        document_chunks = []

        for record in records:

            if (
                record.get("document_id")
                == document_id
            ):

                text = record.get(
                    "text",
                    ""
                )

                if text:
                    document_chunks.append(
                        text
                    )

        if not document_chunks:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No indexed content was found "
                    "for the current document."
                )
            )

        context = "\n\n".join(
            document_chunks
        )

        context = context[:8000]

        recommendations = generate_recommendations(
            context=context
        )

        return {
            "document_id": document_id,
            "recommendations": recommendations
        }

    except HTTPException:
        raise

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Recommendation analysis failed: "
                f"{str(e)}"
            )
        )

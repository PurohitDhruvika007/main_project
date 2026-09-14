from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.schemas.chat_schema import ChatRequest
from app.services.embedding_service import generate_single_embedding
from app.services.vector_store import search_similar_chunks
from app.services.llm_service import generate_answer


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
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


@router.post("/ask")
async def ask_question(
    request: ChatRequest
):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        # Get currently uploaded document
        document_id = get_current_document_id()

        if not document_id:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No document has been uploaded yet. "
                    "Please upload a legal document first."
                )
            )

        # Generate embedding for user's question
        query_embedding = generate_single_embedding(
            request.question
        )

        # Retrieve chunks ONLY from current document
        results = search_similar_chunks(
            query_embedding=query_embedding,
            top_k=3,
            document_id=document_id
        )

        if not results:

            return {
                "question": request.question,
                "answer": (
                    "I could not find relevant information "
                    "in the uploaded document."
                ),
                "document_id": document_id,
                "results": []
            }

        # Build context
        context_parts = []

        for result in results:

            if isinstance(result, dict):

                text = result.get(
                    "text",
                    ""
                )

                if text:
                    context_parts.append(
                        text
                    )

            elif isinstance(result, str):

                context_parts.append(
                    result
                )

        context = "\n\n".join(
            context_parts
        )

        if not context:

            return {
                "question": request.question,
                "answer": (
                    "I could not find relevant "
                    "information in the uploaded document."
                ),
                "document_id": document_id,
                "results": results
            }

        # Limit context before sending to Qwen
        context = context[:5000]

        # Generate document-grounded answer
        answer = generate_answer(
            context=context,
            question=request.question,
            max_new_tokens=100
        )

        return {
            "question": request.question,
            "answer": answer,
            "document_id": document_id,
            "results": results
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
                "Question processing failed: "
                f"{str(e)}"
            )
        )

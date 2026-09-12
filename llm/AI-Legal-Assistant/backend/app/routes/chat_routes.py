from fastapi import APIRouter, HTTPException

from app.schemas.chat_schema import ChatRequest
from app.services.embedding_service import generate_single_embedding
from app.services.vector_store import search_similar_chunks


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/ask")
async def ask_question(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        # Convert user's question into an embedding
        query_embedding = generate_single_embedding(
            request.question
        )

        # Search FAISS for relevant document chunks
        results = search_similar_chunks(
            query_embedding,
            top_k=request.top_k
        )

        return {
            "question": request.question,
            "results": results
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(e)}"
        )

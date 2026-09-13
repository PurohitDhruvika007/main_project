from fastapi import APIRouter, HTTPException

from app.schemas.chat_schema import ChatRequest
from app.services.embedding_service import generate_single_embedding
from app.services.vector_store import search_similar_chunks
from app.services.llm_service import generate_answer


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
        query_embedding = generate_single_embedding(
            request.question
        )

        results = search_similar_chunks(
            query_embedding,
            top_k=request.top_k
        )

        if not results:
            return {
                "question": request.question,
                "answer": "I could not find relevant information in the uploaded document.",
                "results": []
            }

        context_parts = []

        for result in results:
            if isinstance(result, dict):
                text = result.get("text", "")
                if text:
                    context_parts.append(text)
            elif isinstance(result, str):
                context_parts.append(result)

        context = "\n\n".join(context_parts)

        if not context:
            context = str(results)

        answer = generate_answer(
            context=context,
            question=request.question
        )

        return {
            "question": request.question,
            "answer": answer,
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

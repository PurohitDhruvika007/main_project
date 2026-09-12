from fastapi import FastAPI

from app.routes.document_routes import router as document_router
from app.routes.chat_routes import router as chat_router


app = FastAPI(
    title="AI Legal Document Simplifier & Rights Assistant",
    description="AI-based legal document simplification and rights assistance system",
    version="1.0.0"
)


app.include_router(document_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "AI Legal Assistant API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

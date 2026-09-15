from app.routes.recommendation_routes import router as recommendation_router
from app.routes.rights_routes import router as rights_router
from app.routes.chat_routes import router as chat_router
from app.routes.document_routes import router as document_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI(
    title="AI Legal Document Simplifier & Rights Assistant",
    description="AI-based legal document simplification and rights assistance system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(document_router)
app.include_router(chat_router)
app.include_router(rights_router)
app.include_router(recommendation_router)


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

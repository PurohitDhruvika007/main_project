from fastapi import FastAPI

from app.routes.document_routes import router as document_router

from app.routes.chat_routes import router as chat_router

from app.routes.rights_routes import router as rights_router

from app.routes.recommendation_routes import router as recommendation_router


app = FastAPI(

    title="AI Legal Document Simplifier & Rights Assistant",

    description="AI-based legal document simplification and rights assistance system",

    version="1.0.0"

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

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from routes.prediction import router


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title=(
        "AI Road Accident Risk "
        "& Severity Prediction API"
    ),

    description=(
        "Machine Learning API for road "
        "accident severity prediction "
        "and risk analysis."
    ),

    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(
    router
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {

        "message":
            "AI Road Accident Prediction API",

        "status":
            "running",

        "documentation":
            "/docs"
    }

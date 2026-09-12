from fastapi import APIRouter, HTTPException

from schemas.prediction_schema import (
    PredictionRequest
)

from utils.prediction_utils import (
    make_prediction
)


router = APIRouter()


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def health_check():

    return {
        "status": "success",
        "message": "Road Accident ML API is running"
    }


# ============================================================
# PREDICTION
# ============================================================

@router.post("/predict")
def predict_accident(
    request: PredictionRequest
):

    try:

        input_data = (
            request.model_dump()
        )

        result = make_prediction(
            input_data
        )

        return {

            "status": "success",

            "prediction": result
        }

    except Exception as error:

        print(
            "Prediction Error:",
            error
        )

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )

from fastapi import FastAPI, HTTPException

from api.schemas import (
    PredictionRequest,
    PredictionResponse
)

from api.service import predict


app = FastAPI(
    title="Financial ML API",
    version="2.0.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict_route(request: PredictionRequest):
    try:
        result = predict(request.symbol)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
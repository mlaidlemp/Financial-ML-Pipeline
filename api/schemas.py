from pydantic import BaseModel


class PredictionRequest(BaseModel):
    symbol: str


class PredictionResponse(BaseModel):
    symbol: str
    prediction: float
    model_version: str
#This code defines structured request and response formats using Pydantic to ensure correct data types and validation.

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    symbol: str

class PredictionResponse(BaseModel):
    symbol: str
    prediction: int
    probability: float
    
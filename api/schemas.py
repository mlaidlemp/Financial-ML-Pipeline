
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    symbol: str

class PredictionResponse(BaseModel):
    symbol: str
    prediction: int
    probability: float
    timestamp: str
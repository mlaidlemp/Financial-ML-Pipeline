

from fastapi import FastAPI, HTTPException

from api.schemas import PredictionRequest
from api.service import ModelService

from db.init_db import create_price_table
from db.create_feature_table import create_feature_table


print("Initializing database tables...")

create_price_table()
create_feature_table()

print("Database initialization complete")

app = FastAPI(title="Financial ML API")

model_service = ModelService()

@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    try:
        result = model_service.predict(request.symbol)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



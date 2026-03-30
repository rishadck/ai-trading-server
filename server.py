from fastapi import FastAPI
from pydantic import BaseModel
import torch
import numpy as np

app = FastAPI()

class Data(BaseModel):
    symbol: str
    close: list
    rsi: float

# SIMPLE MODEL (placeholder)
class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(21, 3)

    def forward(self, x):
        return self.fc(x)

model = Model()
model.eval()

@app.post("/predict")
def predict(data: Data):
    features = data.close[-20:] + [data.rsi]
    x = torch.tensor(features, dtype=torch.float32)

    out = model(x)
    signal = int(torch.argmax(out))

    return {"signal": signal}
    @app.get("/dashboard")
def dashboard():
    return {
        "status": "running",
        "mode": "AI_PRO",
        "pairs": ["EURUSD","XAUUSD"],
        "version": "v2"
    }

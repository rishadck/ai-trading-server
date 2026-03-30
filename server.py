from fastapi import FastAPI
import torch
import torch.nn as nn
import numpy as np

app = FastAPI()

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 3)

    def forward(self, x):
        return self.fc(x)

model = Model()
model.eval()

@app.get("/")
def home():
    return {"status": "AI server running"}

@app.get("/predict")
def predict(
    p1: float, p2: float, p3: float, p4: float, p5: float,
    p6: float, p7: float, p8: float, p9: float, p10: float
):
    data = np.array([p1,p2,p3,p4,p5,p6,p7,p8,p9,p10])
    x = torch.tensor(data, dtype=torch.float32).unsqueeze(0)

    out = model(x)
    signal = torch.argmax(out).item()

    return {"signal": int(signal)}

from fastapi import FastAPI

app = FastAPI()

# ================= STATUS =================
@app.get("/")
def home():
    return {"status": "AI server running"}

# ================= PREDICT =================
@app.get("/predict")
def predict(
    p1: float, p2: float, p3: float, p4: float, p5: float,
    p6: float, p7: float, p8: float, p9: float, p10: float
):
    # SIMPLE TREND LOGIC (STABLE)
    if p10 > p9:
        signal = 2   # BUY
    elif p10 < p9:
        signal = 0   # SELL
    else:
        signal = 1   # HOLD

    return {
        "signal": signal,
        "strategy": "trend_follow_simple"
    }

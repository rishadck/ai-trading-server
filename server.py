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
    # ================= AUTO THRESHOLD =================
    # Forex pairs (EURUSD etc.) usually < 10
    # Gold (XAUUSD) usually > 1000
    threshold = 0.0002 if p10 < 10 else 0.5

    # ================= LOGIC =================
    if (p10 - p9) > threshold:
        signal = 2   # BUY
    elif (p9 - p10) > threshold:
        signal = 0   # SELL
    else:
        signal = 1   # HOLD

    return {
        "signal": signal,
        "threshold": threshold,
        "strategy": "auto_threshold_trend"
    }

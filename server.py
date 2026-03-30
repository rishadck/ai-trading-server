from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# ================= INPUT MODEL =================
class MarketData(BaseModel):
    symbol: str
    close: list   # last 20 closes
    rsi: float

# ================= HELPER =================
def moving_average(data, period=10):
    return np.mean(data[-period:])

# ================= MAIN LOGIC =================
@app.post("/predict")
def predict(data: MarketData):
    closes = data.close
    rsi = data.rsi

    if len(closes) < 20:
        return {"signal": 1, "reason": "not enough data"}

    # ================= TREND =================
    ma_fast = moving_average(closes, 5)
    ma_slow = moving_average(closes, 15)

    trend_up = ma_fast > ma_slow
    trend_down = ma_fast < ma_slow

    # ================= NOISE FILTER =================
    threshold = 0.0002 if closes[-1] < 10 else 0.5

    move = closes[-1] - closes[-2]

    # ================= MULTI-CANDLE CONFIRM =================
    bullish_candles = sum([1 for i in range(-3, 0) if closes[i] > closes[i-1]])
    bearish_candles = sum([1 for i in range(-3, 0) if closes[i] < closes[i-1]])

    # ================= SNIPER ENTRY =================
    buy_condition = (
        trend_up and
        bullish_candles >= 2 and
        rsi < 35 and
        move > threshold
    )

    sell_condition = (
        trend_down and
        bearish_candles >= 2 and
        rsi > 65 and
        -move > threshold
    )

    # ================= SIGNAL =================
    if buy_condition:
        signal = 2   # BUY
    elif sell_condition:
        signal = 0   # SELL
    else:
        signal = 1   # HOLD

    return {
        "signal": signal,
        "trend": "up" if trend_up else "down",
        "rsi": rsi,
        "candles_up": bullish_candles,
        "candles_down": bearish_candles,
        "strategy": "sniper_pro_v1"
    }

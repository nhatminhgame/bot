from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_API_SECRET"))

def fetch_market_data():
    symbol = os.getenv("SYMBOL", "BNBUSDT")
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=2)
    latest = klines[-1]

    return {
        "timestamp": int(latest[0]),
        "open": float(latest[1]),
        "high": float(latest[2]),
        "low": float(latest[3]),
        "close": float(latest[4]),
        "volume": float(latest[5]),
        "price": float(latest[4]),  # = close price
        "rsi": 52.3,
        "macd": 0.0012,
        "ai_tp_long": 58.2,
        "ai_tp_short": 42.7,
        "trend_1h": "up",
        "trend_4h": "neutral"
    }

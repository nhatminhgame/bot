# utils/candle_buffer.py
import pandas as pd
import ta
import os
from dotenv import load_dotenv
load_dotenv()

from binance.client import Client

candle_buffer = []

def initialize_candle_buffer():
    global candle_buffer
    client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY"))
    klines = client.futures_klines(symbol="BNBUSDT", interval=Client.KLINE_INTERVAL_15MINUTE, limit=100)

    df = pd.DataFrame(klines, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
    ])
    df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})

    # Tính ch? báo
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["ema_fast"] = ta.trend.EMAIndicator(df["close"], window=12).ema_indicator()
    df["ema_slow"] = ta.trend.EMAIndicator(df["close"], window=26).ema_indicator()

    # Luu 10 n?n g?n nh?t
    candle_buffer = []
    for _, row in df.tail(10).iterrows():
        candle_buffer.append({
            "time": row["time"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row["volume"],
            "rsi": row["rsi"],
            "macd": row["macd"],
            "macd_signal": row["macd_signal"],
            "ema_fast": row["ema_fast"],
            "ema_slow": row["ema_slow"],
            "trend": "UP" if row["ema_fast"] > row["ema_slow"] else "DOWN"
        })

def update_candle_buffer(market):
    global candle_buffer
    new_candle = {
        "time": int(pd.Timestamp.now().timestamp() * 1000),
        "open": market["open"],
        "high": market["high"],
        "low": market["low"],
        "close": market["close"],
        "volume": market["volume"],
        "rsi": market.get("rsi", None),
        "macd": market.get("macd", None),
        "macd_signal": market.get("macd_signal", None),
        "ema_fast": market.get("ema_fast", None),
        "ema_slow": market.get("ema_slow", None),
        "trend": "UP" if market.get("ema_fast", 0) > market.get("ema_slow", 0) else "DOWN"
    }
    candle_buffer.append(new_candle)
    if len(candle_buffer) > 10:
        candle_buffer = candle_buffer[-10:]

def get_recent_candles():
    return candle_buffer

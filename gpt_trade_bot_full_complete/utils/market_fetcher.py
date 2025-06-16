from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_API_SECRET"))

def fetch_market_data():
    symbol = os.getenv("SYMBOL", "BNBUSDT")
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=2)

    close_price = float(klines[-1][4])
    volume = float(klines[-1][5])

    # Tạm thời mock chỉ báo – sau có thể tính từ dữ liệu
    return {
        "price": close_price,
        "volume": volume,
        "rsi": 52.3,
        "macd": 0.0012,
        "ai_tp_long": 58.2,
        "ai_tp_short": 42.7,
        "trend_1h": "up",
        "trend_4h": "neutral"
    }

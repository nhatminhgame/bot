from binance.client import Client
from binance.enums import *
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
symbol = os.getenv("SYMBOL", "BNBUSDT")
trade_qty = float(os.getenv("TRADE_QTY", "0.1"))

client = Client(api_key, api_secret)

def place_futures_order(side, reduce_only=False):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=SIDE_BUY if side == "BUY" else SIDE_SELL,
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=trade_qty,
            reduceOnly=reduce_only
        )
        return order
    except Exception as e:
        print("❌ Binance order error:", e)
        return None

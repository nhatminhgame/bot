import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

SYMBOL = os.getenv("SYMBOL", "BNBUSDT")
TRADE_QTY = float(os.getenv("TRADE_QTY", "0.1"))
LEVERAGE = int(os.getenv("LEVERAGE", "4"))
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "0.05"))
GPT_DAILY_LIMIT = int(os.getenv("GPT_DAILY_LIMIT", "50"))
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o")
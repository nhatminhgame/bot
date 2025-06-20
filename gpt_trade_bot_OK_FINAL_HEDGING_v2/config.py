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
GPT_DAILY_LIMIT = int(os.getenv("GPT_DAILY_LIMIT", "100"))
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o")

# ✅ Cấu hình các tính năng nâng cao (mặc định an toàn - không bật)
enable_trailing_stop = False       # Dời SL theo giá khi có lời
enable_dca = False                 # Chia nhiều lệnh LIMIT khi giá đi ngược
enable_smart_reversal = False     # GPT bảo close → đảo chiều
enable_pnl_report = False         # Gửi báo cáo PnL từng lệnh
enable_loss_limit = False         # Giới hạn số lệnh lỗ liên tiếp
enable_gpt_pause_if_static = False  # Dừng GPT nếu thị trường không thay đổi

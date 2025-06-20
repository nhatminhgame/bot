from utils.discord import send_pnl_report
from trade.trade_state import get_position, clear_position
from risk.loss_limiter import record_trade_result
from utils.logger import log_info
import json
from datetime import datetime
import os

TRADE_HISTORY_FILE = "logs/trade_history.json"

def check_tp_sl_hit(current_price: float):
    for side in ["long", "short"]:
        pos = get_position(side)
        if not pos["active"]:
            continue

        entry = pos["entry_price"]
        tp = pos["tp"]
        sl = pos["sl"]

        if side == "long":
            if current_price >= tp:
                _log_trade("long", entry, current_price, "win")
                record_trade_result("win")
                clear_position("long")
                log_info("✅ TP LONG khớp → Win")
            elif current_price <= sl:
                _log_trade("long", entry, current_price, "loss")
                record_trade_result("loss")
                clear_position("long")
                log_info("❌ SL LONG khớp → Loss")

        elif side == "short":
            if current_price <= tp:
                _log_trade("short", entry, current_price, "win")
                record_trade_result("win")
                clear_position("short")
                log_info("✅ TP SHORT khớp → Win")
            elif current_price >= sl:
                _log_trade("short", entry, current_price, "loss")
                record_trade_result("loss")
                clear_position("short")
                log_info("❌ SL SHORT khớp → Loss")

def _log_trade(side, entry, exit, result):
    pnl = ((exit - entry) / entry) * 100 if side == "long" else ((entry - exit) / entry) * 100
    trade = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "side": side,
        "entry": round(entry, 3),
        "exit": round(exit, 3),
        "result": result,
        "pnl_percent": round(pnl, 3)
    }

    os.makedirs("logs", exist_ok=True)
    try:
        with open(TRADE_HISTORY_FILE, "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(trade)

    with open(TRADE_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

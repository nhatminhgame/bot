import json
import os
from config import enable_loss_limit

LIMIT_FILE = "logs/loss_streak.json"
MAX_CONSECUTIVE_LOSSES = 3  # Có thể cấu hình sau

def load_loss_streak():
    if not os.path.exists(LIMIT_FILE):
        return {"loss_streak": 0}
    with open(LIMIT_FILE, "r") as f:
        return json.load(f)

def save_loss_streak(data):
    with open(LIMIT_FILE, "w") as f:
        json.dump(data, f)

def update_loss_streak(pnl):
    data = load_loss_streak()
    if pnl < 0:
        data["loss_streak"] += 1
    else:
        data["loss_streak"] = 0
    save_loss_streak(data)

def is_trading_allowed():
    if not enable_loss_limit:
        return True
    data = load_loss_streak()
    return data["loss_streak"] < MAX_CONSECUTIVE_LOSSES
    
def record_trade_result(pnl):
    update_loss_streak(pnl)
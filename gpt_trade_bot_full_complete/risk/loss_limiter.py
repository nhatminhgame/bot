import json
import os
from datetime import datetime

LOSS_LOG = "logs/loss_log.json"
MAX_CONSECUTIVE_LOSSES = 3
COOLDOWN_MINUTES = 60

def record_trade_result(result: str):
    os.makedirs("logs", exist_ok=True)
    data = _load()
    now = datetime.now().isoformat()

    data["history"].append({"time": now, "result": result})
    if result == "loss":
        data["consecutive_losses"] += 1
    else:
        data["consecutive_losses"] = 0

    if data["consecutive_losses"] >= MAX_CONSECUTIVE_LOSSES:
        data["paused_until"] = (datetime.now().timestamp() + COOLDOWN_MINUTES * 60)

    _save(data)

def is_trade_paused():
    data = _load()
    paused_until = data.get("paused_until", 0)
    return datetime.now().timestamp() < paused_until

def _load():
    if not os.path.exists(LOSS_LOG):
        return {"consecutive_losses": 0, "paused_until": 0, "history": []}
    with open(LOSS_LOG, "r") as f:
        return json.load(f)

def _save(data):
    with open(LOSS_LOG, "w") as f:
        json.dump(data, f)

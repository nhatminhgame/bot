import json
import os
from datetime import datetime

USAGE_FILE = "logs/gpt_usage.json"
LIMIT_PER_DAY = 250

def _load_usage():
    if not os.path.exists(USAGE_FILE):
        return {}
    with open(USAGE_FILE, "r") as f:
        return json.load(f)

def _save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

def can_call_gpt() -> bool:
    data = _load_usage()
    today = datetime.now().strftime("%Y-%m-%d")
    return data.get(today, 0) < LIMIT_PER_DAY

def increment_gpt_usage():
    data = _load_usage()
    today = datetime.now().strftime("%Y-%m-%d")
    data[today] = data.get(today, 0) + 1
    _save_usage(data)

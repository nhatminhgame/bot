import json
import os

STATE_FILE = "logs/trade_state.json"

_state = {
    "long": {
        "entry_price": None,
        "tp": None,
        "sl": None,
        "active": False
    },
    "short": {
        "entry_price": None,
        "tp": None,
        "sl": None,
        "active": False
    }
}

def save_trade_state():
    with open(STATE_FILE, "w") as f:
        json.dump(_state, f)

def load_trade_state():
    global _state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            _state.update(json.load(f))

def set_position(side: str, entry_price: float, tp: float, sl: float):
    _state[side] = {
        "entry_price": entry_price,
        "tp": tp,
        "sl": sl,
        "active": True
    }
    save_trade_state()

def clear_position(side: str):
    _state[side] = {
        "entry_price": None,
        "tp": None,
        "sl": None,
        "active": False
    }
    save_trade_state()

def get_position(side: str):
    return _state[side]

def has_position(side: str):
    return _state[side]["active"]

def get_open_positions(exchange=None, symbol=None):
    """Tra ve danh sach cac vi the dang mo (long / short nếu có)"""
    if exchange is None or symbol is None:
        raise ValueError("Can truyen exchange va symbol vao ham get_open_positions()")

    positions = exchange.fetch_positions()

    open_positions = []
    for p in positions:
        if p["symbol"] == symbol.replace("/", "") and float(p["positionAmt"]) != 0:
            open_positions.append(p)

    return open_positions
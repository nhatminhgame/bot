from collections import deque

CANDLE_LIMIT = 10
_candle_buffer = deque(maxlen=CANDLE_LIMIT)

def update_candle_buffer(candle: dict):
    _candle_buffer.append(candle)

def get_recent_candles() -> list:
    return list(_candle_buffer)

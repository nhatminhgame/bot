import math
from config import enable_trailing_stop

class TrailingStopManager:
    def __init__(self):
        self.active_trailing = {}

    def update(self, position, current_price):
        if not enable_trailing_stop:
            return None  # Không làm gì nếu chưa bật

        symbol = position['symbol']
        side = position['positionSide']
        entry_price = float(position['entryPrice'])
        mark_price = float(current_price)
        key = f"{symbol}_{side}"

        # Lợi nhuận > 0.5% thì mới kích hoạt trailing stop
        change_pct = (mark_price - entry_price) / entry_price * (1 if side == 'LONG' else -1)
        if change_pct < 0.005:
            return None

        # SL sẽ dời lên theo đáy/cao nhất gần đây trừ 0.3%
        trailing_sl_price = mark_price * (1 - 0.003) if side == 'LONG' else mark_price * (1 + 0.003)

        last_sl = self.active_trailing.get(key)
        if last_sl:
            if (side == 'LONG' and trailing_sl_price > last_sl) or (side == 'SHORT' and trailing_sl_price < last_sl):
                self.active_trailing[key] = trailing_sl_price
        else:
            self.active_trailing[key] = trailing_sl_price

        return self.active_trailing[key]
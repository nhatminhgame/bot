from trade.trade_state import get_position, set_position
from utils.logger import log_info

TRAILING_PERCENT = 0.005  # 0.5%

def update_trailing_stop(current_price: float):
    for side in ["long", "short"]:
        pos = get_position(side)
        if not pos["active"]:
            continue

        entry = pos["entry_price"]
        tp = pos["tp"]
        sl = pos["sl"]

        if side == "long":
            new_sl = current_price * (1 - TRAILING_PERCENT)
            if new_sl > sl and current_price > entry:
                set_position("long", entry, tp, new_sl)
                log_info(f"🔁 Dời SL LONG lên {round(new_sl, 3)}")

        elif side == "short":
            new_sl = current_price * (1 + TRAILING_PERCENT)
            if new_sl < sl and current_price < entry:
                set_position("short", entry, tp, new_sl)
                log_info(f"🔁 Dời SL SHORT xuống {round(new_sl, 3)}")

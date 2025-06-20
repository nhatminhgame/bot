from trade.order_manager import OrderManager
from risk.trailing_stop_manager import TrailingStopManager
import json
import os
from utils.logger import log_info
from utils.discord import send_discord_alert

TRADE_STATE_FILE = "trade_state.json"

def save_trade_state(state):
    with open(TRADE_STATE_FILE, "w") as f:
        json.dump(state, f)

def load_trade_state():
    if not os.path.exists(TRADE_STATE_FILE):
        return None
    with open(TRADE_STATE_FILE, "r") as f:
        return json.load(f)

async def execute_gpt_decision(gpt_reply, market):
    action = gpt_reply.get("action")
    confidence = gpt_reply.get("confidence", 0)
    reason = gpt_reply.get("reason", "")

    state = load_trade_state()

    if action == "none" or confidence < 0.55:
        return

    if action == "long":
        if state and state.get("side") == "long":
            return
        place_futures_order("BUY")
        save_trade_state({"side": "long", "entry_price": market["price"]})
        await send_discord_alert(f"🟢 Vào lệnh LONG tại {market['price']} (GPT: {confidence:.2%})\nLý do: {reason}")
        await log_info(f"Vào LONG tại {market['price']}")

    elif action == "short":
        if state and state.get("side") == "short":
            return
        place_futures_order("SELL")
        save_trade_state({"side": "short", "entry_price": market["price"]})
        await send_discord_alert(f"🔴 Vào lệnh SHORT tại {market['price']} (GPT: {confidence:.2%})\nLý do: {reason}")
        await log_info(f"Vào SHORT tại {market['price']}")

    elif action == "close_long" and state and state.get("side") == "long":
        place_futures_order("SELL", reduce_only=True)  # hoặc BUY nếu đang short
        save_trade_state({})
        await send_discord_alert(f"🔁 Đóng lệnh LONG tại {market['price']} (GPT đề xuất)")
        await log_info(f"Thoát LONG tại {market['price']}")

    elif action == "close_short" and state and state.get("side") == "short":
        place_futures_order("SELL", reduce_only=True)  # hoặc BUY nếu đang short
        save_trade_state({})
        await send_discord_alert(f"🔁 Đóng lệnh SHORT tại {market['price']} (GPT đề xuất)")
        await log_info(f"Thoát SHORT tại {market['price']}")



    def place_dca_orders(self, side, base_price, total_size, position_side):
        from config import enable_dca
        if not enable_dca:
            return

        max_levels = 3
        offset_pct = 0.005  # 0.5%
        per_order_size = total_size / max_levels

        for i in range(max_levels):
            level_price = base_price * (1 - offset_pct * (i+1)) if side == "long" else base_price * (1 + offset_pct * (i+1))
            self.exchange.create_limit_order(
                symbol=self.symbol,
                side=side,
                size=per_order_size,
                price=level_price,
                position_side=position_side
            )
            print(f"[DCA] Đặt lệnh DCA {i+1}: {side.upper()} tại giá {level_price:.4f}, size {per_order_size:.4f}")

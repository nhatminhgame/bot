# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from binance.client import Client
from trade.trade_state import has_position, set_position, clear_position
from utils.logger import log_info
from utils.discord import send_discord_message

load_dotenv()
client = Client(
    api_key=os.getenv("BINANCE_API_KEY"),
    api_secret=os.getenv("BINANCE_API_SECRET")
)

symbol = os.getenv("SYMBOL", "BNBUSDT")
qty = float(os.getenv("TRADE_QTY", "0.1"))

async def execute_gpt_decision(gpt_reply: dict, market_data: dict):
    entry_price = market_data["price"]
    action = gpt_reply.get("action", "").lower()

    if action == "long" and not has_position("long"):
        _place_order("BUY", entry_price)
        tp = entry_price * 1.01
        sl = entry_price * 0.985
        set_position("long", entry_price, tp, sl)
        log_info(f"Vao LONG tai {entry_price} | TP: {tp} | SL: {sl}")
        await send_discord_message(f"Vao LONG tai {entry_price:.3f} | TP: {tp:.3f} | SL: {sl:.3f}")

    elif action == "short" and not has_position("short"):
        _place_order("SELL", entry_price)
        tp = entry_price * 0.99
        sl = entry_price * 1.015
        set_position("short", entry_price, tp, sl)
        log_info(f"Vao SHORT tai {entry_price} | TP: {tp} | SL: {sl}")
        await send_discord_message(f"Vao SHORT tai {entry_price:.3f} | TP: {tp:.3f} | SL: {sl:.3f}")

    elif action == "exit":
        if has_position("long"):
            _place_order("SELL", entry_price, reduce_only=True)
            clear_position("long")
            log_info("Thoat LONG theo GPT")
            await send_discord_message("Thoat LONG theo GPT")
        if has_position("short"):
            _place_order("BUY", entry_price, reduce_only=True)
            clear_position("short")
            log_info("Thoat SHORT theo GPT")
            await send_discord_message("Thoat SHORT theo GPT")

    elif action == "reverse_to_long" and has_position("short"):
        _place_order("BUY", entry_price, reduce_only=True)
        clear_position("short")
        log_info("Dao chieu SHORT sang LONG")
        await send_discord_message("Dao chieu SHORT sang LONG")
        await execute_gpt_decision({"action": "long"}, market_data)

    elif action == "reverse_to_short" and has_position("long"):
        _place_order("SELL", entry_price, reduce_only=True)
        clear_position("long")
        log_info("Dao chieu LONG sang SHORT")
        await send_discord_message("Dao chieu LONG sang SHORT")
        await execute_gpt_decision({"action": "short"}, market_data)

def _place_order(side: str, price: float, reduce_only: bool = False):
    try:
        client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=qty,
            reduceOnly=reduce_only
        )
    except Exception as e:
        log_info(f"Loi dat lenh Binance: {e}")
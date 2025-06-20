# main.py - bản sửa lỗi chuẩn

import asyncio
from dotenv import load_dotenv
load_dotenv()

from utils.discord import send_discord_alert
from gpt.gpt_advisor import ask_gpt
from gpt.prompt_formatter import format_market_data_to_prompt
import config
from trade.trade_executor import execute_gpt_decision
from trade.trade_state import load_trade_state
from trade.result_checker import check_tp_sl_hit
from trade.trade_state import get_open_positions
from risk.trailing_stop_manager import TrailingStopManager  # ✅ dùng class
from utils.logger import log_info
from utils.market_fetcher import fetch_market_data
from utils.candle_buffer import update_candle_buffer, get_recent_candles, initialize_candle_buffer
from entry_report import report_no_entry
import os
import json

LAST_GPT_RESULT_PATH = "logs/last_gpt_result.json"
trailing_manager = TrailingStopManager()  # ✅ tạo instance 1 lần

def load_last_gpt_result():
    os.makedirs(os.path.dirname(LAST_GPT_RESULT_PATH), exist_ok=True)
    if not os.path.exists(LAST_GPT_RESULT_PATH):
        return {}
    try:
        with open(LAST_GPT_RESULT_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save_last_gpt_result(result):
    os.makedirs(os.path.dirname(LAST_GPT_RESULT_PATH), exist_ok=True)
    with open(LAST_GPT_RESULT_PATH, "w") as f:
        json.dump(result, f)

async def main_loop():
    await send_discord_alert('Bot GPT Trade đã khởi động và sẵn sàng hoạt động.')

    initialize_candle_buffer()

from config import SYMBOL, BINANCE_API_KEY, BINANCE_API_SECRET, LEVERAGE
from exchange.binance import BinanceExchange  # ho?c dúng class b?n dang dùng

exchange = BinanceExchange(
    api_key=BINANCE_API_KEY,
    api_secret=BINANCE_API_SECRET,
    symbol=SYMBOL,
    leverage=LEVERAGE
)
    symbol = SYMBOL

    while True:
        try:
            market = fetch_market_data()
            update_candle_buffer(market)
            load_trade_state()

            current_price = market["price"]
            check_tp_sl_hit(current_price)

            # ✅ gọi trailing stop nếu cần
            open_positions = get_open_positions(exchange, symbol)
            for pos in open_positions:
                sl = trailing_manager.update(pos, current_price)
                if sl:
                    print(f"[TRAILING] SL dời về {sl:.4f} cho {pos['positionSide']}")


            recent_candles = get_recent_candles()

            if not recent_candles or len(recent_candles) < 5:
                await log_info("recent_candles thiếu dữ liệu, bỏ qua vòng lặp.")
                await asyncio.sleep(60)
                continue

            prompt = format_market_data_to_prompt(market, None, recent_candles)

            await log_info(f"[DEBUG] MARKET INPUT: {market}")
            await log_info(f"[DEBUG] LAST CANDLE: {recent_candles[-1]}")

            gpt_reply = await ask_gpt(prompt)

            await log_info(f"GPT trả lời: {gpt_reply}")
            if gpt_reply.get('action') == 'none':
                await report_no_entry(gpt_reply, market, recent_candles)
            await execute_gpt_decision(gpt_reply, market)

        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            await log_info(f"[LỖI] Chi tiết:\n{trace}")

        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main_loop())

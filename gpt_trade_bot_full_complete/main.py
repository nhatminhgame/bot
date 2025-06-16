# gpt_trade_bot/main.py

import asyncio
from gpt.gpt_advisor import ask_gpt
from gpt.prompt_formatter import format_market_data_to_prompt
from trade.trade_executor import execute_gpt_decision
from trade.trade_state import load_trade_state
from trade.result_checker import check_tp_sl_hit
from risk.trailing_stop_manager import update_trailing_stop
from utils.logger import log_info
from utils.market_fetcher import fetch_market_data
from utils.candle_buffer import update_candle_buffer, get_recent_candles
from entry_report import report_no_entry

async def main_loop():
    from utils.discord import send_discord_message
    send_discord_message('🚀 Bot GPT Trade đã khởi động và sẵn sàng hoạt động.')
    while True:
        try:
            market = fetch_market_data()
            update_candle_buffer(market)  # Cập nhật 10 nến gần nhất
            load_trade_state()  # Đọc trạng thái lệnh hiện tại từ file

            current_price = market["price"]
            check_tp_sl_hit(current_price)  # Kiểm tra TP/SL khớp
            update_trailing_stop(current_price)  # Dời SL nếu có lợi

            recent_candles = get_recent_candles()
            prompt = format_market_data_to_prompt(market, None, recent_candles)
            gpt_reply = await ask_gpt(prompt)

            log_info(f"GPT trả lời: {gpt_reply}")
            if gpt_reply.get('action') == 'none':
                report_no_entry(gpt_reply, market, recent_candles)
            await execute_gpt_decision(gpt_reply, market)

        except Exception as e:
            log_info(f"LỖI: {e}")

        await asyncio.sleep(300)  # 5 phút/lần

if __name__ == "__main__":
    asyncio.run(main_loop())

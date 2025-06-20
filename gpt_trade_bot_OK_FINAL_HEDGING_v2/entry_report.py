# -*- coding: utf-8 -*-
import json
import datetime
from utils.logger import log_info
from utils.discord import send_discord_alert

last_report_time = None

async def report_no_entry(gpt_reply, market, recent_candles):
    global last_report_time

    now = datetime.datetime.now()
    if last_report_time and (now - last_report_time).seconds < 900:
        return

    last_report_time = now

    message = "[ KHÔNG vào lệnh] GPT trả về action: none\n"

    if isinstance(gpt_reply, dict):
        action = gpt_reply.get("action", "none")
        confidence = gpt_reply.get("confidence", 0)
        message += f"• Action: {action}\n"
        message += f"• Confidence: {confidence}\n"
    else:
        message += f"GPT trả về không hợp lệ: {gpt_reply}"

    message += f"\nGiá hiện tại: {market.get('price')}"
    message += f"\nKhung RSI: {market.get('rsi_15m', '?')}, Trend: {market.get('trend', '?')}"

    await send_discord_alert(message)
    await log_info("Đã gửi lý do KHÔNG vào lệnh.")

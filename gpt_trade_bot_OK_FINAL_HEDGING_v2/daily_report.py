# -*- coding: utf-8 -*-
import os
from datetime import datetime
from utils.discord import send_discord_alert

async def send_daily_summary():
    log_file = "logs/gpt_decision_log.json"
    if not os.path.exists(log_file):
        return

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    today = datetime.now().strftime("%Y-%m-%d")
    today_logs = [line for line in lines if today in line]

    long_count = sum(1 for l in today_logs if 'long' in l.lower())
    short_count = sum(1 for l in today_logs if 'short' in l.lower())
    none_count = sum(1 for l in today_logs if 'none' in l.lower())

    message = f" T?ng k?t bot GPT ngày {today}:\n"
    message += f"• L?nh Long: {long_count}\n"
    message += f"• L?nh Short: {short_count}\n"
    message += f"• Không vào l?nh: {none_count}\n"

    await send_discord_alert(message)

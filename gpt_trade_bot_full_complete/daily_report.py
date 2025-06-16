
import os
from datetime import datetime
from utils.discord import send_discord_message

def send_daily_summary():
    log_file = "logs/gpt_decision_log.json"
    if not os.path.exists(log_file):
        return

    with open(log_file, "r") as f:
        lines = f.readlines()

    today = datetime.now().strftime("%Y-%m-%d")
    today_logs = [line for line in lines if today in line]

    long_count = sum(1 for l in today_logs if 'long' in l.lower())
    short_count = sum(1 for l in today_logs if 'short' in l.lower())
    none_count = sum(1 for l in today_logs if 'none' in l.lower())

    message = f"📊 Tổng kết bot GPT ngày {today}:\n"
    message += f"• Lệnh Long: {long_count}\n"
    message += f"• Lệnh Short: {short_count}\n"
    message += f"• Không vào lệnh: {none_count}\n"

    send_discord_message(message)

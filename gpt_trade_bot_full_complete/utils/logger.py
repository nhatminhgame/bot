import os
from datetime import datetime
from utils.discord import send_discord_alert
import asyncio

def log_info(message: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_msg = f"{timestamp} {message}"
    print(full_msg)  # ? Xoá print_color, dùng print thu?ng

    try:
        asyncio.create_task(send_discord_alert(full_msg))
    except Exception as e:
        print(f"[DISCORD ERROR] {e}")

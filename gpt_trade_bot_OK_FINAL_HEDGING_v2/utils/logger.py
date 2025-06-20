# -*- coding: utf-8 -*-
from datetime import datetime
from utils.discord import send_discord_alert

async def log_info(message: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_msg = f"{timestamp} {message}"

    try:
        # Ghi log ra console chu?n UTF-8
        print(full_msg.encode("utf-8", errors="replace").decode("utf-8"))
    except Exception as e:
        print(f"[PRINT ERROR] {e}")

    try:
        await send_discord_alert(full_msg)
    except Exception as e:
        print(f"[DISCORD ERROR] {e}")

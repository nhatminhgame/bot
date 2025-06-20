
import os
from report.generate_report import generate_daily_report
from utils.discord import send_discord_alert
from datetime import datetime
import pytz
import asyncio

async def send_report_if_morning_vn():
    vn_now = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
    if vn_now.hour == 7:
        report = generate_daily_report()
        await send_discord_alert(report)
    else:
        print("⏰ Không phải 7h sáng theo giờ VN, không gửi báo cáo.")

if __name__ == "__main__":
    asyncio.run(send_report_if_morning_vn())

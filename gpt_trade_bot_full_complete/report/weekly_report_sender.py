import os
from report.generate_report import generate_weekly_report
from utils.discord import send_discord_message
from datetime import datetime
import pytz

def send_weekly_report_if_sunday_7am():
    vn_now = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
    if vn_now.weekday() == 6 and vn_now.hour == 7:
        report = generate_weekly_report()
        send_discord_message(report)
    else:
        print("⏰ Không phải Chủ nhật 7h sáng VN → không gửi báo cáo tuần.")

if __name__ == "__main__":
    send_weekly_report_if_sunday_7am()

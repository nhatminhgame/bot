
import requests
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

def send_discord_message(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ DISCORD_WEBHOOK_URL chưa được cấu hình.")
        return

    try:
        payload = {
            "content": message
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"❌ Gửi Discord thất bại: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Lỗi khi gửi Discord: {e}")

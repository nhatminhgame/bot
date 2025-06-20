import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

async def send_discord_alert(message: str):
    if not DISCORD_WEBHOOK_URL:
        print(" DISCORD_WEBHOOK_URL chưa được cấu hình.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            payload = {"content": message}
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as response:
                if response.status != 204 and response.status != 200:
                    print(f"❌ Gửi Discord thất bại: {response.status} - {await response.text()}")
    except Exception as e:
        print(f"❌ Lỗi khi gửi Discord: {e}")


def send_pnl_report(symbol, side, entry_price, exit_price, qty, pnl_usdt, exit_reason):
    color = "🟢" if pnl_usdt >= 0 else "🔴"
    message = f"""{color} **Báo cáo PnL**
• Symbol: {symbol}
• Loại: {side}
• Entry: {entry_price}
• Exit: {exit_price}
• Khối lượng: {qty}
• PnL: {pnl_usdt:.2f} USDT
• Lý do thoát: {exit_reason}
"""
    send_discord_alert(message)

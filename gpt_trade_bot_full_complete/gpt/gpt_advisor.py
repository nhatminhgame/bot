import os
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.logger import log_info
from openai import OpenAI

# ✅ Load biến môi trường .env TRƯỚC KHI dùng
load_dotenv()

# ✅ Lấy config từ biến môi trường
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_DAILY_LIMIT = int(os.getenv("GPT_DAILY_LIMIT", 100))
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY chưa được thiết lập trong .env hoặc biến môi trường!")

# ✅ Tạo client GPT sau khi chắc chắn có API key
client = OpenAI(api_key=OPENAI_API_KEY)

USAGE_FILE = "logs/gpt_usage.json"
DECISION_LOG_FILE = "logs/gpt_decision_log.json"

def _load_usage():
    try:
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"count": 0, "date": ""}

def _save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

def _log_decision(prompt, gpt_reply):
    os.makedirs("logs", exist_ok=True)
    try:
        parsed_reply = json.loads(gpt_reply) if isinstance(gpt_reply, str) else gpt_reply
    except:
        parsed_reply = {"error": "invalid_format", "raw": gpt_reply}

    log = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt,
        "gpt_reply": parsed_reply
    }
    try:
        with open(DECISION_LOG_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
    except:
        data = []

    data.append(log)
    with open(DECISION_LOG_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

async def ask_gpt(prompt: str):
    usage = _load_usage()
    today = datetime.now().strftime("%Y-%m-%d")
    if usage["date"] != today:
        usage = {"count": 0, "date": today}
    if usage["count"] >= GPT_DAILY_LIMIT:
        log_info(" Đã vượt giới hạn GPT daily")
        return {"action": "none", "confidence": 0.0, "reason": "limit_exceeded"}

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": (
                    "Bạn là một chuyên gia giao dịch crypto. "
                    "Trả lời ngắn gọn bằng JSON với chỉ 2 trường: action và confidence. "
                    "Ví dụ: {\"action\": \"long\", \"confidence\": 0.82}. "
                    "Các lựa chọn hợp lệ cho action là: long, short, exit, none."
                )},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        usage["count"] += 1
        _save_usage(usage)

        reply_text = response.choices[0].message.content.strip()
        # Xử lý nếu GPT trả về trong khối ```json ... ```
        if reply_text.startswith("```"):
            reply_text = reply_text.strip("`").strip()
            if reply_text.lower().startswith("json"):
                reply_text = reply_text[4:].strip()  # Bỏ 'json' nếu có
        log_info(f"GPT RAW: {reply_text}")
        _log_decision(prompt, reply_text)

        try:
            reply_json = json.loads(reply_text)
            assert isinstance(reply_json, dict) and "action" in reply_json
        except Exception as e:
            log_info(f" GPT trả về sai định dạng: {e}")
            reply_json = {"action": "none", "confidence": 0.0, "reason": "format_error"}

        return reply_json

    except Exception as e:
        log_info(f"❌ Lỗi GPT: {e}")
        return {"action": "none", "confidence": 0.0, "reason": "api_error"}

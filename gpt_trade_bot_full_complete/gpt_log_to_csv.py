# gpt_log_to_csv.py
import json
import pandas as pd
from pathlib import Path

def extract_gpt_log_to_csv(
    log_path="logs/gpt_decision_log.json",
    output_csv="logs/gpt_training_dataset.csv"
):
    log_file = Path(log_path)
    if not log_file.exists():
        print(f"❌ Không tìm thấy file: {log_path}")
        return

    with open(log_file, "r", encoding="utf-8") as f:
        log_data = json.load(f)

    training_data = []
    for entry in log_data:
        prompt = entry.get("prompt", "")
        reply = entry.get("gpt_reply", {})

        if isinstance(reply, str):
            try:
                reply = json.loads(reply)
            except:
                continue

        action = reply.get("action", "")
        reason = reply.get("reason", "")
        confidence = reply.get("confidence", None)

        if action and confidence is not None:
            training_data.append({
                "prompt": prompt,
                "action": action,
                "reason": reason,
                "confidence": confidence
            })

    df = pd.DataFrame(training_data)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"✅ Đã tạo file CSV: {output_csv} với {len(df)} dòng dữ liệu.")

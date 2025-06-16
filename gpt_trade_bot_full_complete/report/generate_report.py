import json
from datetime import datetime, timedelta

TRADE_HISTORY_FILE = "logs/trade_history.json"

def load_history():
    try:
        with open(TRADE_HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def summarize_trades(start_date: datetime):
    trades = load_history()
    if not isinstance(trades, list):
        return {"count": 0, "win": 0, "loss": 0, "pnl": 0.0}

    summary = {"count": 0, "win": 0, "loss": 0, "pnl": 0.0}
    for t in trades:
        try:
            if not isinstance(t, dict) or "time" not in t:
                continue
            trade_time = datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S")
            if trade_time >= start_date:
                summary["count"] += 1
                summary["pnl"] += t.get("pnl_percent", 0.0)
                if t.get("result") == "win":
                    summary["win"] += 1
                else:
                    summary["loss"] += 1
        except Exception as e:
            print(f"[ B? qua l?nh l?i] {e} ? {t}")
            continue

    return summary

def generate_daily_report():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    s = summarize_trades(today)
    return f"""
 **BÁO CÁO NGÀY {today.strftime('%Y-%m-%d')}**
- T?ng l?nh: {s['count']}
- Win: {s['win']} | Loss: {s['loss']}
- PnL t?ng: {round(s['pnl'], 2)}%
"""

def generate_weekly_report():
    week_ago = datetime.now() - timedelta(days=7)
    s = summarize_trades(week_ago)
    return f"""
 **BÁO CÁO 7 NGÀY QUA**
- T?ng l?nh: {s['count']}
- Win: {s['win']} | Loss: {s['loss']}
- PnL t?ng: {round(s['pnl'], 2)}%
"""

from utils.indicator_summary import summarize_indicators

def format_market_data_to_prompt(market: dict, position: dict, recent_candles: list):
    indicators_15m = summarize_indicators(market, timeframe="15m")
    indicators_1h = summarize_indicators(market, timeframe="1h")
    indicators_4h = summarize_indicators(market, timeframe="4h")

    candle_data = "\n".join([
        f"{c.get('time', '???')}: O={c.get('open', '?')}, H={c.get('high', '?')}, L={c.get('low', '?')}, C={c.get('close', '?')}, Vol={c.get('volume', '?')}"
        for c in recent_candles
    ])

    position_text = "Không có vị thế hiện tại."
    if position:
        position_text = f"Đang giữ vị thế {position['side']} tại giá {position['entry_price']}"

    return f"""
Dữ liệu kỹ thuật:
• 15m: {indicators_15m}
• 1h: {indicators_1h}
• 4h: {indicators_4h}

Lịch sử 10 nến gần nhất:
{candle_data}

{position_text}

Hãy trả lời bằng JSON gồm: action (long, short, close_long, close_short, pause), reason, confidence (0–1), optional: risk_adjustment (float), exit_reason (str).
"""

# -*- coding: utf-8 -*-
from utils.indicator_summary import summarize_indicators

def format_market_data_to_prompt(market: dict, position: dict, recent_candles: list):
    indicators_15m = summarize_indicators(market, timeframe="15m")
    indicators_1h = summarize_indicators(market, timeframe="1h")
    indicators_4h = summarize_indicators(market, timeframe="4h")

    candle_data = "\n".join([
        f"{c.get('time', '???')}: close={c.get('close', '?')}, rsi={c.get('rsi', '?')}, macd={c.get('macd', '?')}, macd_signal={c.get('macd_signal', '?')}, ema_fast={c.get('ema_fast', '?')}, ema_slow={c.get('ema_slow', '?')}, vol={c.get('volume', '?')}, trend={c.get('trend', '?')}"
        for c in recent_candles
    ])

    position_text = "Không có vị thế hiện tại."
    if position:
        position_text = f"Đang giữ vị thế {position['side']} tại giá {position['entry_price']}"

    return f"""
 DỮ LIỆU KỸ THUẬT:
• 15m: {indicators_15m}
• 1h: {indicators_1h}
• 4h: {indicators_4h}

 10 NẾN GẦN NHẤT:
{candle_data}

 TRẠNG THÁI LỆNH:
{position_text}

HÃY PHÂN TÍCH:
1. Dựa trên chuỗi RSI, MACD, EMA, volume, đánh giá xu hướng thị trường hiện tại.
2. Có tín hiệu rõ ràng để vào lệnh không? Long hay Short?
3. Tự đánh giá mức độ tự tin (confidence) từ 0 đến 1.
4. Nếu không nên vào lệnh, hãy nêu rõ lý do (ví dụ: thị trường sideway, tín hiệu xung đột, dữ liệu chưa đủ).
5. Nếu nên vào lệnh, nêu rõ lý do và đề xuất hành động phù hợp.

TRẢ VỀ JSON DUY NHẤT theo định dạng:
{{
  "action": "long" | "short" | "none" | "close",
  "confidence": 0.xx,
  "reason": "..."  ← giải thích rõ vì sao chọn action (bắt buộc nếu action là 'none')
}}
"""
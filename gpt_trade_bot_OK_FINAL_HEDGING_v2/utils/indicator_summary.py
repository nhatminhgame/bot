def summarize_indicators(market, timeframe="15m"):
    # Giả định: lấy dữ liệu từ market["indicators"][timeframe]
    data = market.get("indicators", {}).get(timeframe, {})
    summary = f"RSI: {data.get('rsi', '?')}, EMA: {data.get('ema', '?')}, MACD: {data.get('macd', '?')}"
    return summary

# GPT Trade Bot - Full Real Trading System

## 📦 Các chức năng chính:
- Gọi GPT-4o để quyết định lệnh mỗi 5 phút (LONG/SHORT/EXIT/NONE)
- Đặt lệnh thực tế trên Binance Futures (hedging mode: long + short cùng lúc)
- Giới hạn gọi GPT theo ngày, trailing stop, kiểm soát rủi ro
- Gửi báo cáo & cảnh báo qua Discord
- Ghi log toàn bộ prompt & phản hồi GPT
- Huấn luyện AI nội bộ từ log để thay GPT

## ▶️ Cách sử dụng:
1. Cài thư viện:
```bash
pip install -r requirements.txt
```

2. Tạo file `.env` từ `.env.example`, điền:
```
OPENAI_API_KEY=
BINANCE_API_KEY=
BINANCE_API_SECRET=
DISCORD_WEBHOOK_URL=
SYMBOL=BNBUSDT
TRADE_QTY=0.1
LEVERAGE=4
RISK_PER_TRADE=0.05
GPT_DAILY_LIMIT=50
GPT_MODEL=gpt-4o
```

3. Chạy bot:
```bash
python main.py
```

4. Tạo dataset từ GPT log:
```bash
python gpt_log_to_csv.py
```

5. Train AI nội bộ:
```bash
python train_gpt_ai_model.py
```

## 📁 Các thư mục:
- `gpt/`: xử lý GPT
- `trade/`: quản lý lệnh
- `risk/`: trailing stop, limit lỗ
- `report/`: báo cáo ngày/tuần
- `utils/`: log, Discord, chỉ báo
- `logs/`: GPT log
- `models/`: AI model nội bộ

---

Liên hệ để mở rộng thêm tính năng như Telegram, đa coin, UI Web.

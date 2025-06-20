import time

class OrderManager:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol

    def has_open_position(self, position_side):
        positions = self.exchange.fetch_positions()
        for p in positions:
            if p['symbol'] == self.symbol.replace("/", "") and p['positionSide'] == position_side:
                if float(p['positionAmt']) != 0:
                    return True
        return False

    def place_market_order_with_sl_tp(self, side, size, sl_price, tp_price, position_side):
        print(f"[ORDER] MARKET {side.upper()} | SL: {sl_price:.4f} | TP: {tp_price:.4f}")

        self.exchange.create_market_order(
            symbol=self.symbol,
            side=side,
            size=size,
            position_side=position_side
        )

        # Đặt SL
        self.exchange.create_stop_loss_order(
            symbol=self.symbol,
            side="sell" if side == "long" else "buy",
            stop_price=sl_price,
            position_side=position_side
        )

        # Đặt TP
        self.exchange.create_take_profit_order(
            symbol=self.symbol,
            side="sell" if side == "long" else "buy",
            take_profit_price=tp_price,
            position_side=position_side
        )
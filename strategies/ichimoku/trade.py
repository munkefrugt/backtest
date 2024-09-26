# trade.py

class Trade:
    def __init__(self, trade_id, symbol, buy_price, stop_loss, target, position_size, buy_time):
        self.trade_id = trade_id
        self.symbol = symbol
        self.buy_price = buy_price
        self.stop_loss = stop_loss
        self.target = target
        self.position_size = position_size
        self.buy_time = buy_time
        self.status = 'open'
        self.close_time = None
        self.close_price = None

    def close_trade(self, close_time, close_price):
        self.status = 'closed'
        self.close_time = close_time
        self.close_price = close_price
        print(f"Closing trade {self.trade_id} at time: {close_time} with price: {close_price}")

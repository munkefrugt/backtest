import pandas as pd
import numpy as np
from trade import Trade
from plot_backtest import plot_backtest
 
class BacktestSimulator:
    def __init__(self, initial_cash):
        self.previous_dc_20_high = None
        self.previous_ema_200 = None
        self.previous_ema_5000 = None
        self.previous_sema_20000 = None
        self.previous_chikou_past = None
        self.cash = initial_cash
        self.equity = initial_cash
        self.trades = []
        self.buy_signals = []
        self.sell_signals = []
        self.cash_equity_records = []
        self.profits = []
        self.drawdowns = []
        self.current_drawdown = 0
        self.max_equity = initial_cash
        self.winning_streak = 0
        self.losing_streak = 0
        self.max_winning_streak = 0
        self.max_losing_streak = 0
        self.current_streak_type = None

    def run_backtest(self, df):
        df['equity'] = self.cash
        df['chikou_above_cloud_3_bars'] = df['chikou_26_past'] > df[['senkou_a_26_past', 'senkou_b_26_past']].max(axis=1)
        df['chikou_above_cloud_3_bars'] = df['chikou_above_cloud_3_bars'].rolling(window=3).sum() == 3

        for index, row in df.iterrows():
            self.row_simulator(row)
        return df, pd.DataFrame(self.cash_equity_records, columns=['date', 'cash', 'equity', 'position'])

    def calculate_position_size(self, equity, cash, current_price, stop_loss, risk_percentage=0.02):
        risk_amount = equity * risk_percentage
        risk_per_share = current_price - stop_loss
        position_size_risk = risk_amount / risk_per_share
        position_size_cash = cash / current_price
        final_position_size = min(position_size_risk, position_size_cash)
        return final_position_size

    def row_simulator(self, row):
        current_time = row['date']
        current_price = row['close']
        dc_20_high = row['Donchian_20_high']
        current_ema_50 = row['EMA_50']
        current_ema_200 = row['EMA_200']
        current_ema_5000 = row['EMA_5000']
        current_ema_20000 = row['EMA_20000']
        symbol = "BTC-USD"
        
        chikou_past = row['chikou_26_past']
        senkou_a_past = row['senkou_a_26_past']
        senkou_b_past = row['senkou_b_26_past']
        senkou_a_future = row['senkou_a_future']
        senkou_b_future = row['senkou_b_future']
        senkou_a = row['ichimoku_a']
        senkou_b = row['ichimoku_b']

        currentCloudTop = max(senkou_a, senkou_b)
        pastCloudTop = max(senkou_a_past, senkou_b_past)

        equity = self.cash
        for open_trade in self.trades:
            if open_trade.status == 'open':
                value_of_position = open_trade.position_size * current_price
                equity += value_of_position

        self.max_equity = max(self.max_equity, equity)
        self.current_drawdown = (self.max_equity - equity) / self.max_equity
        self.drawdowns.append(self.current_drawdown)

        already_in_trade = any(trade.status == 'open' for trade in self.trades)

        if not already_in_trade and self.previous_chikou_past is not None:
            if row['chikou_above_cloud_3_bars']:
                if current_price > current_ema_50 > current_ema_200 > current_ema_5000 > current_ema_20000:
                    if self.previous_ema_200 < current_ema_200:
                        if chikou_past > pastCloudTop:
                            if current_price > currentCloudTop:
                                if senkou_a_future > senkou_b_future:
                                    if current_price > self.previous_dc_20_high:
                                        if current_price > senkou_a > senkou_b:
                                            trade_id = len(self.trades) + 1
                                            stop_loss = min(senkou_a, senkou_b)
                                            position_size = self.calculate_position_size(equity, self.cash, current_price, stop_loss, risk_percentage=0.02)
                                            trade = Trade(trade_id, symbol, current_price, stop_loss, current_price + (current_price - stop_loss) * 1.5, position_size, current_time)
                                            value_of_position = position_size * current_price
                                            self.cash -= value_of_position
                                            self.trades.append(trade)
                                            self.buy_signals.append((current_time, current_price))

        for trade in self.trades:
            if trade.status == 'open':
                if chikou_past < row['close_26_past'] or senkou_a_future < senkou_b_future:
                    self.sell(trade, current_time, current_price)
        self.previous_dc_20_high = dc_20_high
        self.previous_ema_200 = current_ema_200
        self.previous_ema_5000 = current_ema_5000
        self.previous_ema_20000 = current_ema_20000
        self.previous_chikou_past = chikou_past

        self.cash_equity_records.append([current_time, self.cash, equity, 0])

    def sell(self, trade, current_time, current_price):
        trade.close_trade(current_time, current_price)
        self.sell_signals.append((current_time, current_price))
        value_of_position = trade.position_size * current_price
        self.cash += value_of_position
        trade.status = 'closed'
        profit = value_of_position - (trade.position_size * trade.buy_price)

        self.profits.append(profit)
        self.update_streak(profit)
        print(f'Profit: {profit}')

    def update_streak(self, profit):
        if profit > 0:
            if self.current_streak_type == 'win':
                self.winning_streak += 1
            else:
                self.winning_streak = 1
                self.losing_streak = 0
            self.current_streak_type = 'win'
        else:
            if self.current_streak_type == 'loss':
                self.losing_streak += 1
            else:
                self.losing_streak = 1
                self.winning_streak = 0
            self.current_streak_type = 'loss'

        self.max_winning_streak = max(self.max_winning_streak, self.winning_streak)
        self.max_losing_streak = max(self.max_losing_streak, self.losing_streak)

    def get_stats(self):
        num_trades = len(self.profits)
        num_wins = len([p for p in self.profits if p > 0])
        win_rate = num_wins / num_trades if num_trades > 0 else 0
        avg_profit = np.mean(self.profits) if self.profits else 0
        max_drawdown = max(self.drawdowns) if self.drawdowns else 0

        return {
            "win_rate": win_rate,
            "average_profit": avg_profit,
            "max_drawdown": max_drawdown,
            "max_winning_streak": self.max_winning_streak,
            "max_losing_streak": self.max_losing_streak
        }


def load_old_training_data():
    path = '/home/martin/Documents/backtest/data/reduced_data_with_ichimoku.csv'
    df = pd.read_csv(path, low_memory=False)
    return df

def filter_data_by_ema_slope(df):
    # Calculate slope of the 5000-period EMA
    df['EMA_5000_slope'] = df['EMA_5000'].diff()
    
    # Calculate slope of the 1000-period EMA
    df['EMA_1000_slope'] = df['EMA_1000'].diff()
    
    # Apply the filter: Keep rows where both EMA_5000 and EMA_1000 slopes are positive
    # and EMA_20000 is less than or equal to EMA_5000
    filtered_df = df[
        (df['EMA_5000_slope'] > 0) & 
        (df['EMA_1000_slope'] > 0) & 
        (df['EMA_20000'] <= df['EMA_5000'])
    ]
    
    # Optionally drop the slope columns if they are no longer needed
    filtered_df = filtered_df.drop(columns=['EMA_5000_slope', 'EMA_1000_slope'])
    
    return filtered_df


# Usage:
df = load_old_training_data()
df = df.tail(20000)  # Process last 10,000 rows for example


#print(df)
#df = df.head(100)  # Process last 10,000 rows for example
df['chikou_26_past'] = df['close']
df['senkou_a_26_past'] = df['ichimoku_a'].shift(26)
df['senkou_b_26_past'] = df['ichimoku_b'].shift(26)

df['senkou_a_future'] = df['ichimoku_a'].shift(-26)
df['senkou_b_future'] = df['ichimoku_b'].shift(-26)

df['close_26_past'] = df['close'].shift(26)



columns_to_display = ['date', 'close', 'chikou_26_past','ichimoku_a', 'ichimoku_b','senkou_a_26_past', 'senkou_b_26_past']  # Replace with your actual column names
pd.set_option('display.max_rows', 50)

#print(df[columns_to_display].head(50))

df = filter_data_by_ema_slope(df)


# # Run backtest
simulator = BacktestSimulator(initial_cash=1000)
df, cash_equity_df = simulator.run_backtest(df)

# # Get and print stats
stats = simulator.get_stats()
print(stats)

plot_backtest(df, simulator.buy_signals, simulator.sell_signals, cash_equity_df)

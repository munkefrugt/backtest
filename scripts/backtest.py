#from load_history import load_old_training_data
from plot_backtest import plot_backtest
from trade import Trade
import pandas as pd

#test
previous_price = None
previous_ema_200 = None
previous_resistance = None
second_previous_resistance = None
previous_support = None
don_low_5 = None
don_low_10 = None

resistance_levels = []
buy_signals = []
sell_signals = []
trades = []
cash_equity_df = pd.DataFrame(columns=['timestamp', 'cash', 'equity', 'position'])
#breakout_limit_df = pd.DataFrame(columns=['timestamp', 'breakout_limit'])

cash = 1000
equity = None
def run_backtest(df):
    global cash_equity_df

    df = df.reset_index()
    for index, row in df.iterrows():
        row_checker(row)
    print(cash_equity_df.tail(1))
    return df, cash_equity_df

def calculate_position_size(equity, cash, current_price, stop_loss, risk_percentage=0.02):
    # Calculate the amount you're willing to risk
    risk_amount = equity * risk_percentage
    
    # Calculate the risk per share
    risk_per_share = current_price - stop_loss
    
    # Calculate position size based on risk
    position_size_risk = risk_amount / risk_per_share
    
    # Calculate position size based on available cash
    position_size_cash = cash / current_price
    
    # Final position size should be the minimum of the two
    final_position_size = min(position_size_risk, position_size_cash)
    
    return final_position_size

def is_stable_resistance_level(resistance_levels, minutes):
    if len(resistance_levels) < minutes:
        return False
    last_x_values = resistance_levels[-minutes:]
    return all(value == last_x_values[0] for value in last_x_values)

def row_checker(row):
    global previous_price, previous_ema_200, previous_resistance, second_previous_resistance, previous_support, resistance_levels, don_low_5, don_low_10, cash_equity_df, cash

    current_time = row['timestamp']
    current_price = row['close_price']
    current_ema_200 = row['EMA_200']
    symbol = row['symbol']
    resistance = row["Resistance"]
    support = row["Support"]

    don_low_10 = row["Donchian_10_low"]
    don_low_5 = row["Donchian_5_low"]

    # Update equity
    equity = cash
    for open_trade in trades:
        if open_trade.status == 'open':
            value_of_position = open_trade.position_size * current_price
            equity += value_of_position

    # Update resistance_levels list
    if previous_resistance is not None:
        resistance_levels.append(previous_resistance)
    
    # Buy
    if cash >= 1:
        if is_stable_resistance_level(resistance_levels, 20):  # Check the last 20 resistance levels
            max_resistance = resistance_levels[-1]

            if previous_resistance is not None and second_previous_resistance is not None and previous_support is not None:
                if current_price > previous_resistance and max_resistance == previous_resistance:
                    difference_between_resistance_and_support = previous_resistance - previous_support
                    percentage_over_resistance = 0.1
                    breakout_limit = previous_support + difference_between_resistance_and_support * (1 + percentage_over_resistance)
                    if current_price > breakout_limit:
                        trade_id = len(trades) + 1
                        stop_loss = don_low_10
                        risk = current_price - stop_loss
                        target = current_price + risk * 1.5
                        position_size = calculate_position_size(equity, cash, current_price, stop_loss, risk_percentage=0.02)
                        trade = Trade(trade_id, symbol, current_price, stop_loss, target, position_size, current_time)
                        value_of_position = position_size * current_price
                        cash -= value_of_position
                        trades.append(trade)
                        buy_signals.append((current_time, current_price))

    # Sell
    if previous_price and previous_ema_200 is not None:
        for trade in trades:
            if trade.status == 'open':
                if current_price < trade.stop_loss:
                    sell(trade, current_time, current_price)
                elif current_price >= trade.target:
                    sell(trade, current_time, current_price)

    previous_price = current_price
    previous_ema_200 = current_ema_200
    second_previous_resistance = previous_resistance
    previous_resistance = resistance
    previous_support = support
    
    new_cash_equity_row = pd.DataFrame({'timestamp': [current_time], 'cash': [cash], 'equity': [equity], 'position': [0]})
    cash_equity_df = pd.concat([cash_equity_df, new_cash_equity_row], ignore_index=True)

def sell(trade,current_time,current_price):
    global cash
    trade.close_trade(current_time, current_price)
    sell_signals.append((current_time, current_price))
    value_of_position= trade.position_size * current_price
    cash += value_of_position
    trade.status = 'closed'
    start_value = trade.position_size * trade.buy_price
    profit = value_of_position -start_value 
    print('profit : ' + str(profit))


def load_old_training_data():
    print("load_old_training_data")
    #path = "/home/martin/Documents/pyhtonPaperTrade/historic_stream_plot_BTC/Backtest_testFile.csv"
    path = '/home/martin/Documents/pyhtonPaperTrade/historic_stream_plot_BTC/newTestData.csv'
    df = pd.read_csv(path, low_memory=False)
    #df = df.tail(2000)
    df['symbol'] = 'BTC/USDT'
    df["symbol"] = df["symbol"].astype(str)
    df["order_status"] = df["order_status"].astype(str)
    return df




df = load_old_training_data()
# minimize data. sort out negative EMA1000
# Shift the EMA_1000 column to create a comparison column
df['EMA_1000_previous'] = df['EMA_1000'].shift(1)

# Keep only rows where the current EMA_1000 is greater than or equal to the previous value
df = df[df['EMA_1000'] >= df['EMA_1000_previous']]

# Drop the helper column as it's no longer needed
df = df.drop(columns=['EMA_1000_previous'])
#df = df.tail(3000)

df, cash_equity_df = run_backtest(df)
plot_backtest(df, buy_signals, sell_signals, cash_equity_df,)


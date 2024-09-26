#from load_history import load_old_training_data
from plot_backtest import plot_backtest
from trade import Trade
import pandas as pd
import plotly.graph_objects as go


#test
previous_price = None
previous_ema_5000 = None
previous_ema_20000 = None

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
        row_simulator(row)
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


def row_simulator(row):
    global previous_ema_5000, previous_ema_20000, cash_equity_df, cash

    current_time = row['date']
    current_price = row['close']
    #current_ema_200 = row['EMA_200']
    current_ema_5000 = row['EMA_5000']
    current_ema_20000 = row['EMA_20000']
    symbol = "BTC-USD"

    # Update equity
    equity = cash
    for open_trade in trades:
        if open_trade.status == 'open':
            value_of_position = open_trade.position_size * current_price
            equity += value_of_position


    # Buy
    if cash >= 1:
        if previous_ema_5000 is not None: 
            if current_ema_5000 > current_ema_20000 and previous_ema_5000 < previous_ema_20000:
                trade_id = len(trades) + 1
                stop_loss = current_ema_5000
                risk = current_price - stop_loss
                target = current_price + risk * 1.5
                position_size = calculate_position_size(equity, cash, current_price, stop_loss, risk_percentage=0.02)
                trade = Trade(trade_id, symbol, current_price, stop_loss, target, position_size, current_time)
                value_of_position = position_size * current_price
                cash -= value_of_position
                trades.append(trade)
                buy_signals.append((current_time, current_price))

    # Sell
    for trade in trades:
        if trade.status == 'open':
            if current_price < trade.stop_loss:
                sell(trade, current_time, current_price)
            elif current_price >= trade.target:
                sell(trade, current_time, current_price)

    previous_ema_5000  = current_ema_5000
    previous_ema_20000  = current_ema_20000


    
    new_cash_equity_row = pd.DataFrame({'date': [current_time], 'cash': [cash], 'equity': [equity], 'position': [0]})
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
    path = '/home/martin/Documents/backtest/reduced_data_with_ichimoku.csv'

    df = pd.read_csv(path, low_memory=False)
    #df = df.tail(2000)
    #df['symbol'] = 'BTC/USDT'
    #df["symbol"] = df["symbol"].astype(str)
    #df["order_status"] = df["order_status"].astype(str)
    return df



def fast_plot(df):

    # Create a figure
    fig = go.Figure()

    # Add Close Price trace
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close Price', line=dict(color='blue')))

    # Add EMA 200 trace
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_200'], mode='lines', name='EMA 200', line=dict(color='red')))

    # Add EMA 1000 trace
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_1000'], mode='lines', name='EMA 1000', line=dict(color='green')))
    
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_5000'], mode='lines', name='EMA 5000', line=dict(color='purple')))

    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_20000'], mode='lines', name='EMA 5000', line=dict(color='black')))

    # Update layout for title and axis labels
    fig.update_layout(
        title='Close Price, EMA 200, and EMA 1000',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis=dict(tickangle=45),
        legend_title='Legend',
        template='plotly_white',
        width=1000, height=600
    )

    # Show the plot
    fig.show()

def coarse_filter(df):
# minimize data. full set is 3160089 rows
    df = df[df['EMA_1000'] > df['EMA_5000']]

    return df

#Main:

df = load_old_training_data()

#df = coarse_filter(df)
#print(df.columns)
#print(df.tail(10))
#print(df)
df = df.tail(10000)
#df = df.tail(300000)
#df = df.head(300000)
#fast_plot(df)


df, cash_equity_df = run_backtest(df)
plot_backtest(df, buy_signals, sell_signals, cash_equity_df,)

# Index(['date', 'open', 'high', 'low', 'close', 'ichimoku_base_line',
#        'ichimoku_conversion_line', 'ichimoku_a', 'ichimoku_b', 'EMA_50',
#        'EMA_200', 'EMA_1000', 'EMA_5000', 'EMA_20000'],
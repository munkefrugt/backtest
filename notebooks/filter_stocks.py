import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import math

# Step 1: Define the top 50 S&P 500 stocks by market cap
top_50_stocks = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'BRK-B', 'JPM', 'JNJ', 
    'V', 'WMT', 'PG', 'UNH', 'DIS', 'HD', 'MA', 'PYPL', 'BAC', 'VZ', 
    'ADBE', 'NFLX', 'INTC', 'CMCSA', 'PFE', 'KO', 'CSCO', 'PEP', 'ABT', 'NKE', 
    'XOM', 'MRK', 'T', 'CVX', 'MDT', 'ABBV', 'LLY', 'CRM', 'ACN', 'AVGO', 
    'MCD', 'COST', 'WFC', 'TXN', 'NEE', 'HON', 'UNP', 'QCOM', 'ORCL'
]

# Step 2: Function to fetch and prepare daily data
def get_daily_data(symbol):
    df = yf.download(symbol, period='1y', interval='1d')
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    return df

# Step 3: Fetch daily data for all top 50 stocks
daily_data = {stock: get_daily_data(stock) for stock in top_50_stocks}

# Step 4: Function to check for a recent EMA Golden Cross within the last 10 days
def has_recent_golden_cross(df):
    for i in range(1, 11):  # Check the last 10 days
        if df['EMA_50'].iloc[-i] > df['EMA_200'].iloc[-i] and df['EMA_50'].iloc[-(i+1)] <= df['EMA_200'].iloc[-(i+1)]:
            return True
    return False

# Step 5: Filter stocks that have had a recent Golden Cross
filtered_stocks = [stock for stock, data in daily_data.items() if has_recent_golden_cross(data)]

print(f"Stocks with a recent EMA Golden Cross within the last 10 days: {filtered_stocks}")

# Step 6: Plot the daily data for the filtered stocks (max 6 per figure)
stocks_per_figure = 6
num_figures = math.ceil(len(filtered_stocks) / stocks_per_figure)

for fig_num in range(num_figures):
    plt.figure(figsize=(14, 10))
    
    # Get the current batch of stocks to plot in this figure
    start_idx = fig_num * stocks_per_figure
    end_idx = start_idx + stocks_per_figure
    current_batch = filtered_stocks[start_idx:end_idx]
    
    for i, stock in enumerate(current_batch, 1):
        plt.subplot(len(current_batch), 1, i)
        df = daily_data[stock]
        plt.plot(df['Close'], label='Close Price', color='black')
        plt.plot(df['EMA_50'], label='EMA 50', color='blue')
        plt.plot(df['EMA_200'], label='EMA 200', color='red')
        
        plt.title(f'{stock} - Daily Timeframe')
        plt.legend(loc='best')

    plt.tight_layout()
    plt.show()

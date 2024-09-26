import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the CSV file into a pandas DataFrame
file_path = '/home/martin/Documents/data/BTC-USD_minute_2012-2018/btc-usd-minute2012-18.csv'
df = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Set the 'date' column as the DataFrame index for resampling
df.set_index('date', inplace=True)

# Calculate EMA 200 on the minute-level data
df['EMA_200_minute'] = df['close'].ewm(span=200, adjust=False).mean()

# Resample data to hourly, 4-hourly, and daily timeframes
df_hourly = df.resample('H').agg({'close': 'mean'})
df_4hourly = df.resample('4H').agg({'close': 'mean'})
df_daily = df.resample('D').agg({'close': 'mean'})

# Calculate EMA 200 for hourly, 4-hourly, and daily data
df_hourly['EMA_200_hourly'] = df_hourly['close'].ewm(span=200, adjust=False).mean()
df_4hourly['EMA_200_4hourly'] = df_4hourly['close'].ewm(span=200, adjust=False).mean()
df_daily['EMA_200_daily'] = df_daily['close'].ewm(span=200, adjust=False).mean()

# Merge the data to align the timeframes
df_merged = df_hourly[['EMA_200_hourly']].merge(df_4hourly[['EMA_200_4hourly']], how='outer', left_index=True, right_index=True)
df_merged = df_merged.merge(df_daily[['EMA_200_daily']], how='outer', left_index=True, right_index=True)

# Forward-fill to align daily/4-hourly EMA with hourly data
df_merged.fillna(method='ffill', inplace=True)

# Create a condition for when the trend is up (EMA hierarchy holds)
df_merged['trend_signal'] = np.where((df_merged['EMA_200_hourly'] > df_merged['EMA_200_4hourly']) & 
                                     (df_merged['EMA_200_4hourly'] > df_merged['EMA_200_daily']), 1, 0)

# Extract the dates where the signal is true
signal_dates = df_merged[df_merged['trend_signal'] == 1].index
signal_prices = df_hourly.loc[signal_dates, 'close']

# Create the plot
fig = make_subplots(rows=1, cols=1)

# Add the close price and EMA lines
fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Close Price (Minute)', line=dict(color='blue', width=1), opacity=0.5))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA_200_minute'], mode='lines', name='EMA 200 (Minute)', line=dict(color='red', width=1)))
fig.add_trace(go.Scatter(x=df_hourly.index, y=df_hourly['EMA_200_hourly'], mode='lines', name='EMA 200 (Hourly)', line=dict(color='green', width=1)))
fig.add_trace(go.Scatter(x=df_4hourly.index, y=df_4hourly['EMA_200_4hourly'], mode='lines', name='EMA 200 (4-Hourly)', line=dict(color='orange', width=1)))
fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['EMA_200_daily'], mode='lines', name='EMA 200 (Daily)', line=dict(color='black', width=1)))

# Add signals (markers) where the trend condition holds
fig.add_trace(go.Scatter(x=signal_dates, y=signal_prices, mode='markers', name='Trend Signal', 
                         marker=dict(color='green', size=10, symbol='triangle-up')))

# Update layout
fig.update_layout(
    title="Close Price with EMA 200 and Trend Signals",
    xaxis_title="Date",
    yaxis_title="Price",
    xaxis_rangeslider_visible=False,
    template="plotly_white",
)

# Show the plot
fig.show()

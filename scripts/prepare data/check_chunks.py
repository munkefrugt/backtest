import pandas as pd
import matplotlib.pyplot as plt

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

# Plotting the close price and EMAs
plt.figure(figsize=(12, 8))

# Minute-level close price and EMA
plt.plot(df.index, df['close'], label='Close Price (Minute)', color='blue', alpha=0.5)
plt.plot(df.index, df['EMA_200_minute'], label='EMA 200 (Minute)', color='red')

# Hourly EMA 200
plt.plot(df_hourly.index, df_hourly['EMA_200_hourly'], label='EMA 200 (Hourly)', color='green')

# 4-Hourly EMA 200
plt.plot(df_4hourly.index, df_4hourly['EMA_200_4hourly'], label='EMA 200 (4-Hourly)', color='orange')

# Daily EMA 200
plt.plot(df_daily.index, df_daily['EMA_200_daily'], label='EMA 200 (Daily)', color='black')

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Close Price with EMA 200 (Minute, Hourly, 4-Hourly, and Daily)')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the legend
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.show()

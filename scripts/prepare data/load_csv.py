import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
file_path = 'data_with_ichimoku.csv'
df = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Calculate EMA200 and EMA1000
df['EMA_200'] = df['close'].ewm(span=200, adjust=False).mean()
df['EMA_1000'] = df['close'].ewm(span=1000, adjust=False).mean()

# Initialize variables for chunk counting
current_trend = None
chunks = 0

# Iterate through the DataFrame to count chunks (EMA200 > EMA1000 or EMA200 < EMA1000)
for index, row in df.iterrows():
    ema_200 = row['EMA_200']
    ema_1000 = row['EMA_1000']
    
    # Determine the current trend
    trend = 'bullish' if ema_200 > ema_1000 else 'bearish'

    # Check if the trend changes, which defines a chunk
    if current_trend is None:
        current_trend = trend
    elif trend != current_trend:
        chunks += 1
        current_trend = trend

# Output the number of chunks
print(f'Number of chunks where trends change (EMA200 crosses EMA1000): {chunks}')

# Plotting the close price, EMA200, and EMA1000
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['close'], label='Close Price', color='blue')
plt.plot(df['date'], df['EMA_200'], label='EMA 200', color='red')
plt.plot(df['date'], df['EMA_1000'], label='EMA 1000', color='green')

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Close Price, EMA 200, and EMA 1000')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the legend
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.show()

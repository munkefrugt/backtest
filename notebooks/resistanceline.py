import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Step 1: Define the stock symbol and fetch daily data for the last year
symbol = 'AAPL'
df = yf.download(symbol, period='2y', interval='1d')

# Step 2: Identify local tops (peaks) in the closing price
peaks, _ = find_peaks(df['Close'], distance=20)  # `distance` parameter controls the minimum separation between peaks
df['Peaks'] = np.nan
df['Peaks'].iloc[peaks] = df['Close'].iloc[peaks]

# Step 3: Filter peaks that are close to each other to form a resistance level
tolerance = 0.01  # 1% tolerance to group peaks as a single resistance level
resistance_candidates = df['Peaks'].dropna()
resistance_levels = []

# Loop over the identified peaks and group them into resistance levels
for i, peak in enumerate(resistance_candidates):
    close_price = resistance_candidates.iloc[i]
    
    # Check if this peak is close to an existing resistance level within the tolerance
    if any(abs(close_price - level) / level < tolerance for level in resistance_levels):
        continue
    
    # Otherwise, consider this peak as a new resistance level
    resistance_levels.append(close_price)

# Calculate the resistance line as the mean of the grouped resistance levels
resistance_line = np.mean(resistance_levels) if resistance_levels else None

# Step 4: Plot the data along with the resistance line
plt.figure(figsize=(14, 7))
plt.plot(df['Close'], label='Close Price', color='black')
plt.plot(df['Peaks'], 'ro', label='Tops')

# If a resistance line was identified, plot it
if resistance_line:
    plt.axhline(y=resistance_line, color='green', linestyle='--', label='Resistance Line')
else:
    print("No significant resistance line identified.")

plt.title(f'{symbol} - Daily Timeframe with Identified Resistance')
plt.legend(loc='best')
plt.show()

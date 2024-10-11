import pandas as pd
import matplotlib.pyplot as plt

def calculate_manual_ichimoku(df):
    """Calculate Tenkan-sen, Kijun-sen, Senkou Span A, and Senkou Span B manually."""
    
    # Tenkan-sen (Conversion Line) - Midpoint of 9-period high-low
    df['tenkan_sen'] = (df['high'].rolling(window=9).max() + df['low'].rolling(window=9).min()) / 2

    # Kijun-sen (Base Line) - Midpoint of 26-period high-low
    df['kijun_sen'] = (df['high'].rolling(window=26).max() + df['low'].rolling(window=26).min()) / 2

    # Senkou Span A (Leading Span A) - Average of Tenkan-sen and Kijun-sen, shifted 26 periods forward
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)

    # Senkou Span B (Leading Span B) - Midpoint of 52-period high-low, shifted 26 periods forward
    df['senkou_span_b'] = ((df['high'].rolling(window=52).max() + df['low'].rolling(window=52).min()) / 2).shift(26)

    return df

def preprocess_data(file_path):
    """Preprocess the data by calculating Ichimoku indicators manually."""
    df = pd.read_csv(file_path)

    # Limit the data to the first 200 rows
    df = df.head(200)

    # Calculate Ichimoku manually
    df = calculate_manual_ichimoku(df)

    return df

def plot_ichimoku(df):
    """Plot Tenkan-sen, Kijun-sen, and Ichimoku Cloud for visual inspection."""
    plt.figure(figsize=(10, 6))
    
    # Plot the close price
    plt.plot(df['close'], label='Close Price', color='black', linewidth=1.5)

    # Plot Tenkan-sen and Kijun-sen
    plt.plot(df['tenkan_sen'], label='Tenkan-sen (Conversion Line)', linestyle='--', color='blue')
    plt.plot(df['kijun_sen'], label='Kijun-sen (Base Line)', linestyle='--', color='red')

    # Plot Senkou Span A and Senkou Span B (Cloud)
    plt.plot(df['senkou_span_a'], label='Senkou Span A', linestyle='--', color='green')
    plt.plot(df['senkou_span_b'], label='Senkou Span B', linestyle='--', color='orange')

    # Fill the cloud area between Senkou Span A and Senkou Span B
    plt.fill_between(df.index, df['senkou_span_a'], df['senkou_span_b'], where=(df['senkou_span_a'] >= df['senkou_span_b']),
                     color='lightgreen', alpha=0.4)
    plt.fill_between(df.index, df['senkou_span_a'], df['senkou_span_b'], where=(df['senkou_span_a'] < df['senkou_span_b']),
                     color='lightcoral', alpha=0.4)

    # Add labels and legend
    plt.title('Ichimoku: Tenkan-sen, Kijun-sen, and Cloud (First 200 Rows)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Example usage: preprocess the CSV and plot Ichimoku lines
    input_file = '/home/martin/Documents/data/SPXUSD/SPXUSD_2010_to_2018.csv'
    df = preprocess_data(input_file)

    # Plot the calculated Tenkan-sen, Kijun-sen, and Cloud
    plot_ichimoku(df)

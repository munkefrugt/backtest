import pandas as pd

def calculate_manual_ichimoku(df):
    """Manually calculate Ichimoku Cloud indicators and add them to the dataframe."""
    
    # Tenkan-sen (Conversion Line) - Midpoint of 9-period high-low
    df['ichimoku_conversion_line'] = (df['high'].rolling(window=9).max() + df['low'].rolling(window=9).min()) / 2

    # Kijun-sen (Base Line) - Midpoint of 26-period high-low
    df['ichimoku_base_line'] = (df['high'].rolling(window=26).max() + df['low'].rolling(window=26).min()) / 2

    # Senkou Span A (Leading Span A) - Average of Tenkan-sen and Kijun-sen, shifted 26 periods forward
    df['ichimoku_a'] = ((df['ichimoku_conversion_line'] + df['ichimoku_base_line']) / 2).shift(26)

    # Senkou Span B (Leading Span B) - Midpoint of 52-period high-low, shifted 26 periods forward
    df['ichimoku_b'] = ((df['high'].rolling(window=52).max() + df['low'].rolling(window=52).min()) / 2).shift(26)

    # Chikou Span (Lagging Span) - The close price shifted 26 periods backward
    df['ichimoku_chikou_line'] = df['close'].shift(-26)

    return df

def calculate_ema(df, periods=200):
    """Calculate Exponential Moving Average (EMA)."""
    df[f'EMA_{periods}'] = df['close'].ewm(span=periods, adjust=False).mean()
    return df

def calculate_donchian_channel(df, window=20):
    """Calculate Donchian Channel for a given window."""
    df[f'Donchian_{window}_high'] = df['high'].rolling(window=window).max()
    df[f'Donchian_{window}_low'] = df['low'].rolling(window=window).min()
    return df

def preprocess_data(file_path, output_file, strategy='ichimoku'):
    """Preprocess the data by calculating necessary indicators."""
    df = pd.read_csv(file_path)
    
    if strategy == 'ichimoku':
        df = calculate_manual_ichimoku(df)
    
    # Calculate Donchian Channels for different windows
    df = calculate_donchian_channel(df, window=26)
    df = calculate_donchian_channel(df, window=20)
    df = calculate_donchian_channel(df, window=10)  # Add both 10 and 20 period Donchian
    
    # Calculate some common indicators like EMA
    df = calculate_ema(df, periods=50)
    df = calculate_ema(df, periods=200)
    df = calculate_ema(df, periods=1000)
    df = calculate_ema(df, periods=5000)
    df = calculate_ema(df, periods=20000)
    df = calculate_ema(df, periods=50000)


    # Save the processed file with a specific name indicating the strategy used
    df.to_csv(output_file, index=False)
    print(f"Indicators calculated and saved to {output_file}")

if __name__ == "__main__":
    # Example usage: preprocess a CSV with Ichimoku indicators
    input_file = '/home/martin/Documents/data/SPXUSD/SPXUSD_2010_to_2018.csv'
    output_file = 'SPX_USD_2010_18_minute_ichimoku_EMA_DC.csv'
    preprocess_data(input_file, output_file, strategy='ichimoku')

    # You can also run for Donchian Channel
    #output_file = 'data_with_donchian.csv'
    #preprocess_data(input_file, output_file, strategy='donchian')

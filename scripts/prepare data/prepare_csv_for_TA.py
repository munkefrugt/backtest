import pandas as pd
import ta  # Using the 'ta' library to calculate common indicators like Ichimoku and EMA

def calculate_ichimoku(df):
    """Calculate Ichimoku Cloud indicators and add them to the dataframe."""
    ichimoku = ta.trend.IchimokuIndicator(
        high=df['high'], low=df['low'], window1=9, window2=26, window3=52
    )
    df['ichimoku_base_line'] = ichimoku.ichimoku_base_line()
    df['ichimoku_conversion_line'] = ichimoku.ichimoku_conversion_line()
    df['ichimoku_a'] = ichimoku.ichimoku_a()
    df['ichimoku_b'] = ichimoku.ichimoku_b()
    df['ichimoku_chikou_line'] = df['close'].shift(-26)  # Shift the close price 26 periods backward

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
    
    df = calculate_ichimoku(df)
    df = calculate_donchian_channel(df, window=20)
    df = calculate_donchian_channel(df, window=10)  # Add both 10 and 20 period Donchian
    
    # Calculate some common indicators like EMA (you can extend this)
    df = calculate_ema(df, periods=50)
    df = calculate_ema(df, periods=200)
    df = calculate_ema(df, periods=1000)
    df = calculate_ema(df, periods=5000)
    df = calculate_ema(df, periods=20000)

    #df = df.tail(300000)

    # Save the processed file with a specific name indicating the strategy used
    df.to_csv(output_file, index=False)
    print(f"Indicators calculated and saved to {output_file}")

if __name__ == "__main__":
    # Example usage: preprocess a CSV with Ichimoku indicators
    input_file = '/home/martin/Documents/data/BTC-USD_minute_2012-2018/btc-usd-minute2012-18.csv'
    output_file = 'data_with_ichimoku.csv'
    preprocess_data(input_file, output_file, strategy='ichimoku')

    # You can also run for Donchian Channel
    #output_file = 'data_with_donchian.csv'
    #preprocess_data(input_file, output_file, strategy='donchian')

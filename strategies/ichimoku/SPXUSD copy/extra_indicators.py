# Calculate EMA slopes and acceleration
def calculate_ema_slopes(df):
    df['EMA_50_slope'] = df['EMA_50'].diff()  # First derivative (slope)
    df['EMA_200_slope'] = df['EMA_200'].diff()
    df['EMA_1000_slope'] = df['EMA_1000'].diff()
    df['EMA_5000_slope'] = df['EMA_5000'].diff()
    df['EMA_20000_slope'] = df['EMA_20000'].diff()

    df['meta_ema_slope_200_ema_50'] = df['EMA_50_slope'].ewm(span=50, adjust=False).mean()
    df['meta_ema_slope_200_ema_200'] = df['EMA_200_slope'].ewm(span=200, adjust=False).mean()
    df['meta_ema_slope_1000_ema_200'] = df['EMA_1000_slope'].ewm(span=200, adjust=False).mean()

    return df

def get_more_ichimoku_indicators(df):
    # Add Ichimoku past/future data
    df['chikou_26_past'] = df['close']
    df['senkou_a_26_past'] = df['ichimoku_a'].shift(26)
    df['senkou_b_26_past'] = df['ichimoku_b'].shift(26)
    df['senkou_a_future'] = df['ichimoku_a'].shift(-26)
    df['senkou_b_future'] = df['ichimoku_b'].shift(-26)
    df['close_26_past'] = df['close'].shift(26)
    return df

def get_extra_donchian(df):
    df['Donchian_100_high'] = df['high'].rolling(window=100).max()
    df['Donchian_200_high'] = df['high'].rolling(window=200).max()
    df['Donchian_500_high'] = df['high'].rolling(window=500).max()
    df['Donchian_1000_high'] = df['high'].rolling(window=1000).max()
    df['Donchian_3day_high'] = df['high'].rolling(window=4320).max()


    #low
    df['Donchian_50_low'] = df['low'].rolling(window=50).min()
    df['Donchian_100_low'] = df['low'].rolling(window=100).min()
    df['Donchian_200_low'] = df['low'].rolling(window=200).min()
    df['Donchian_500_low'] = df['low'].rolling(window=500).min()
    return df

def get_ema(df):
    df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['EMA_100'] = df['close'].ewm(span=100, adjust=False).mean()
    df['EMA_300'] = df['close'].ewm(span=300, adjust=False).mean()
    df['EMA_500'] = df['close'].ewm(span=500, adjust=False).mean()
    df['EMA_100000'] = df['close'].ewm(span=100000, adjust=False).mean()

    return df

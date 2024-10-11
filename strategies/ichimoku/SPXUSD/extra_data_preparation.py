# Calculate EMA slopes and acceleration
def calculate_ema_slopes(df):
    df['EMA_50_slope'] = df['EMA_50'].diff()  # First derivative (slope)
    df['EMA_200_slope'] = df['EMA_200'].diff()
    df['EMA_1000_slope'] = df['EMA_1000'].diff()
    df['EMA_5000_slope'] = df['EMA_5000'].diff()
    df['EMA_20000_slope'] = df['EMA_20000'].diff()

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
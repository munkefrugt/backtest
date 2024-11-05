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
    df['senkou_a_26_past'] = df['ichimoku_a'].shift(26)
    df['senkou_b_26_past'] = df['ichimoku_b'].shift(26)
    df['senkou_a_future'] = df['ichimoku_a'].shift(-26)
    df['senkou_b_future'] = df['ichimoku_b'].shift(-26)
    df['close_26_past'] = df['close'].shift(26)
    df['chikou_26_past'] = df['close'].shift(-26)

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
    df['EMA_9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['EMA_21'] = df['close'].ewm(span=21, adjust=False).mean()
    df['EMA_100'] = df['close'].ewm(span=100, adjust=False).mean()
    df['EMA_300'] = df['close'].ewm(span=300, adjust=False).mean()
    df['EMA_500'] = df['close'].ewm(span=500, adjust=False).mean()
    df['EMA_2000'] = df['close'].ewm(span=2000, adjust=False).mean()
    df['EMA_3000'] = df['close'].ewm(span=3000, adjust=False).mean()
    df['EMA_100000'] = df['close'].ewm(span=100000, adjust=False).mean()

    return df

# Function to calculate Kaufman's Adaptive Moving Average (KAMA)
def calculate_kama(df, window, fast, slow, column_name):
    df['change'] = df['close'].diff()
    df['volatility'] = df['change'].abs().rolling(window=window).sum()
    df['direction'] = abs(df['close'].diff(periods=window))
    
    df['efficiency_ratio'] = df['direction'] / df['volatility']
    df['smoothing_constant'] = ((df['efficiency_ratio'] * (2 / (fast + 1) - 2 / (slow + 1)) + 2 / (slow + 1)) ** 2)
    
    df[column_name] = df['close']
    for i in range(window, len(df)):
        df[column_name].iat[i] = df[column_name].iat[i - 1] + df['smoothing_constant'].iat[i] * (df['close'].iat[i] - df[column_name].iat[i - 1])

    # Clean up the temporary columns
    df.drop(columns=['change', 'volatility', 'direction', 'efficiency_ratio', 'smoothing_constant'], inplace=True)
    
    return df

def apply_kamas(df):
    # Short-term KAMA
    df = calculate_kama(df, window=21, fast=2, slow=21, column_name='KAMA_short')
    
    # Medium-term KAMA
    df = calculate_kama(df, window=50, fast=5, slow=50, column_name='KAMA_medium')
    
    # Long-term KAMA
    df = calculate_kama(df, window=100, fast=10, slow=70, column_name='KAMA_long')
    
    df = calculate_kama(df, window=1000, fast=10, slow=70, column_name='KAMA_extra_long')

    return df

def add_extra_indicators(df):
    df = get_ema(df)
    df = calculate_ema_slopes(df)
    df = get_more_ichimoku_indicators(df)
    df = get_extra_donchian(df)
    df = apply_kamas(df)  # Add KAMA calculation here
    return df
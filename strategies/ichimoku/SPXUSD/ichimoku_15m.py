import pandas as pd

def process_and_merge_ichimoku_15min(minute_df, date_column='date'):
    """
    Processes the minute-level data to calculate the 15-minute Ichimoku cloud 
    and merge it into the minute-level data.

    :param minute_df: A DataFrame containing minute-level price data.
    :param date_column: The name of the datetime column.
    :return: A DataFrame with the 15-minute Ichimoku cloud data merged into the minute-level data, with a common integer index.
    """

    # Step 1: Resample to 15-minute intervals
    def resample_to_15min(df, date_column):
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.set_index(date_column)
        df_15min = df.resample('15T').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()
        return df_15min

    # Step 2: Calculate Ichimoku Cloud for 15-minute data
    def calculate_ichimoku_15min(df):
        high_9 = df['high'].rolling(window=9).max()
        low_9 = df['low'].rolling(window=9).min()
        high_26 = df['high'].rolling(window=26).max()
        low_26 = df['low'].rolling(window=26).min()
        high_52 = df['high'].rolling(window=52).max()
        low_52 = df['low'].rolling(window=52).min()

        # Tenkan-sen (Conversion Line)
        tenkan_sen_15min = (high_9 + low_9) / 2

        # Kijun-sen (Base Line)
        kijun_sen_15min = (high_26 + low_26) / 2

        # Senkou Span A (Leading Span A)
        senkou_a_15min = ((tenkan_sen_15min + kijun_sen_15min) / 2).shift(26)

        # Senkou Span B (Leading Span B)
        senkou_b_15min = ((high_52 + low_52) / 2).shift(26)

        senkou_a_15min_future = senkou_a_15min.shift(-26)
        senkou_b_15min_future = senkou_b_15min.shift(-26)

        # Chikou Span (Lagging Span)
        chikou_span_15min = df['close'].shift(-26)

        # Calculate the 26-period past values for Chikou, Senkou A, and Senkou B
        chikou_span_26_past_15min = chikou_span_15min.shift(26)
        senkou_a_26_past_15min = senkou_a_15min.shift(26)
        senkou_b_26_past_15min = senkou_b_15min.shift(26)

        close_15min = df['close']

        ichimoku_df = pd.DataFrame({
            'senkou_a_15min': senkou_a_15min,
            'senkou_b_15min': senkou_b_15min,
            'senkou_a_15min_future': senkou_a_15min_future,
            'senkou_b_15min_future': senkou_b_15min_future,
            'chikou_span_15min': chikou_span_15min,
            'kijun_sen_15min': kijun_sen_15min,
            'tenkan_sen_15min': tenkan_sen_15min,
            'chikou_26_past_15min': chikou_span_26_past_15min,  # Past Chikou
            'senkou_a_26_past_15min': senkou_a_26_past_15min,  # Past Senkou A
            'senkou_b_26_past_15min': senkou_b_26_past_15min,   # Past Senkou B
            'close_15min': close_15min
        })

        return ichimoku_df.dropna()

    # Step 3: Merge the 15-minute Ichimoku cloud data into the minute-level data
    def merge_15min_ichimoku(df, df_15min, date_column):
        # Convert the date column to datetime
        df[date_column] = pd.to_datetime(df[date_column])

        # Ensure minute-level data has datetime set as the index
        df = df.set_index(date_column)

        # Merge 15-minute Ichimoku data into minute-level data
        df = pd.merge_asof(df, df_15min, left_index=True, right_index=True, direction='backward')

        # Reset the index and create a common integer index
        df = df.reset_index()

        return df

    def add_15min_block_marker(df, date_column):
        # Create the 15-minute block marker
        df['15min_block'] = pd.to_datetime(df[date_column]).dt.floor('15T')
        return df

    # Process
    df_15min = resample_to_15min(minute_df, date_column)
    df_ichimoku_15min = calculate_ichimoku_15min(df_15min)
    merged_df = merge_15min_ichimoku(minute_df, df_ichimoku_15min, date_column)
    merged_df = add_15min_block_marker(merged_df, date_column)

    # Create a common integer index
    merged_df['index'] = range(1, len(merged_df) + 1)
    merged_df = merged_df.set_index('index')

    return merged_df

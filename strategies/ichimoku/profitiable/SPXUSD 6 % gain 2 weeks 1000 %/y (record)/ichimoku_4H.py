import pandas as pd

def process_and_merge_ichimoku(minute_df, date_column='date'):
    """
    Processes the minute-level data to calculate the 4-hour Ichimoku cloud and merge it into the minute-level data.

    :param minute_df: A DataFrame containing minute-level price data.
    :param date_column: The name of the datetime column.
    :return: A DataFrame with the 4-hour Ichimoku cloud data merged into the minute-level data, with a common integer index.
    """
    
    # Step 1: Resample to 4-hour intervals
    def resample_to_4h(df, date_column):
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.set_index(date_column)
        df_4h = df.resample('4H').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()
        return df_4h

    # Step 2: Calculate Ichimoku Cloud for 4-hour data
    def calculate_ichimoku_4h(df):
        high_9 = df['high'].rolling(window=9).max()
        low_9 = df['low'].rolling(window=9).min()
        high_26 = df['high'].rolling(window=26).max()
        low_26 = df['low'].rolling(window=26).min()
        high_52 = df['high'].rolling(window=52).max()
        low_52 = df['low'].rolling(window=52).min()

        # Tenkan-sen (Conversion Line)
        tenkan_sen_4H = (high_9 + low_9) / 2

        # Kijun-sen (Base Line)
        kijun_sen_4H = (high_26 + low_26) / 2

        # Senkou Span A (Leading Span A)
        senkou_a_4H = ((tenkan_sen_4H + kijun_sen_4H) / 2).shift(26)

        # Senkou Span B (Leading Span B)
        senkou_b_4H = ((high_52 + low_52) / 2).shift(26)

        senkou_a_4H_future = senkou_a_4H.shift(-26)
        senkou_b_4H_future = senkou_b_4H.shift(-26)

        # Chikou Span (Lagging Span)
        chikou_span_4H = df['close'].shift(-26)

        # Calculate the 26-period past values for Chikou, Senkou A, and Senkou B
        chikou_span_26_past_4H = chikou_span_4H.shift(26)
        senkou_a_26_past_4H = senkou_a_4H.shift(26)
        senkou_b_26_past_4H = senkou_b_4H.shift(26)

        close_4H = df['close']

        ichimoku_df = pd.DataFrame({
            'senkou_a_4H': senkou_a_4H,
            'senkou_b_4H': senkou_b_4H,
            'senkou_a_4H_future': senkou_a_4H_future,
            'senkou_b_4H_future': senkou_b_4H_future,
            'chikou_span_4H': chikou_span_4H,
            'kijun_sen_4H': kijun_sen_4H,
            'tenkan_sen_4H': tenkan_sen_4H,
            'chikou_26_past_4H': chikou_span_26_past_4H,  # Past Chikou
            'senkou_a_26_past_4H': senkou_a_26_past_4H,  # Past Senkou A
            'senkou_b_26_past_4H': senkou_b_26_past_4H,   # Past Senkou B
            'close_4H' : close_4H
        })

        return ichimoku_df.dropna()

    # Step 3: Merge the 4-hour Ichimoku cloud data into the minute-level data
    def merge_4H_ichimoku(df, df_4h, date_column):
        # Convert the date column to datetime
        df[date_column] = pd.to_datetime(df[date_column])

        # Ensure minute-level data has datetime set as the index
        df = df.set_index(date_column)

        # Merge 4-hour Ichimoku data into minute-level data
        df = pd.merge_asof(df, df_4h, left_index=True, right_index=True, direction='backward')

        # Reset the index and create a common integer index
        df = df.reset_index()

        return df

    def add_4h_block_marker(df, date_column):
        # Create the 4-hour block marker
        df['4H_block'] = pd.to_datetime(df[date_column]).dt.floor('4H')
        return df

    # Process
    df_4h = resample_to_4h(minute_df, date_column)
    df_ichimoku_4h = calculate_ichimoku_4h(df_4h)
    merged_df = merge_4H_ichimoku(minute_df, df_ichimoku_4h, date_column)
    merged_df = add_4h_block_marker(merged_df, date_column)

    # Shift by 26 4-hour blocks to get the detailed Chikou Span
    #merged_df['detailed_chikou_4H'] = merged_df.groupby('4H_block')['close'].shift(-26)

    # Create a common integer index
    merged_df['index'] = range(1, len(merged_df) + 1)
    merged_df = merged_df.set_index('index')

    return merged_df

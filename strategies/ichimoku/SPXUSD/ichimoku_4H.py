import pandas as pd

def process_and_merge_ichimoku(minute_df, date_column='datetime'):
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


        ichimoku_df = pd.DataFrame({
            'senkou_a_4H': senkou_a_4H,
            'senkou_b_4H': senkou_b_4H,
            'senkou_a_4H_future': senkou_a_4H_future,
            'senkou_b_4H_future': senkou_b_4H_future,

            'chikou_span_4H': chikou_span_4H,
            'kijun_sen_4H': kijun_sen_4H,
            'tenkan_sen_4H': tenkan_sen_4H
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

    # Process
    df_4h = resample_to_4h(minute_df, date_column)
    df_ichimoku_4h = calculate_ichimoku_4h(df_4h)
    merged_df = merge_4H_ichimoku(minute_df, df_ichimoku_4h, date_column)

    # Create a common integer index
    merged_df['index'] = range(1, len(merged_df) + 1)
    merged_df = merged_df.set_index('index')

    return merged_df

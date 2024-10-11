from dateutil.relativedelta import relativedelta
import pandas as pd


# Filter data by date range
def filter_data_by_date_range(df, start_year, start_month, months=6):
    df['date'] = pd.to_datetime(df['date'])
    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)
    end_date = start_date + relativedelta(months=months)
    return df[(df['date'] >= start_date) & (df['date'] < end_date)]


# Filter based on EMA slopes
def filter_data_by_ema_slope(df, ema_5000_threshold=0.01, ema_1000_threshold=0.01, ema_20000_threshold=0.0001):
    
    # Apply the filter based on slope values
    filtered_df = df[
        (df['EMA_5000_slope'] > ema_5000_threshold) & 
        (df['EMA_1000_slope'] > ema_1000_threshold) & 
        (df['EMA_20000_slope'] > ema_20000_threshold)
    ]
    
    return filtered_df
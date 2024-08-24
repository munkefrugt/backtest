import numpy as np
import pandas as pd
from ta.trend import EMAIndicator
from ta.volatility import DonchianChannel


def compute_ta_indicators(df):
    """Compute technical analysis indicators for the given DataFrame."""
    df['EMA_50'] = EMAIndicator(close=df['close_price'], window=50).ema_indicator()
    df['EMA_100'] = EMAIndicator(close=df['close_price'], window=100).ema_indicator()
    df['EMA_200'] = EMAIndicator(close=df['close_price'], window=200).ema_indicator()
    df['EMA_1000'] = EMAIndicator(close=df['close_price'], window=1000).ema_indicator()



    donchian_5 = DonchianChannel(high=df['high_price'], low=df['low_price'], close=df['close_price'], window=5)
    df['Donchian_5_high'] = donchian_5.donchian_channel_hband()
    df['Donchian_5_low'] = donchian_5.donchian_channel_lband()

    donchian_10 = DonchianChannel(high=df['high_price'], low=df['low_price'], close=df['close_price'], window=10)
    df['Donchian_10_high'] = donchian_10.donchian_channel_hband()
    df['Donchian_10_low'] = donchian_10.donchian_channel_lband()

    donchian_20 = DonchianChannel(high=df['high_price'], low=df['low_price'], close=df['close_price'], window=20)
    df['Donchian_20_high'] = donchian_20.donchian_channel_hband()
    df['Donchian_20_low'] = donchian_20.donchian_channel_lband()

    donchian_100 = DonchianChannel(high=df['high_price'], low=df['low_price'], close=df['close_price'], window=100)
    df['Donchian_100_high'] = donchian_100.donchian_channel_hband()
    df['Donchian_100_low'] = donchian_100.donchian_channel_lband()

    # Compute support and resistance levels
    df['Support'], df['Resistance'] = compute_support_resistance(df)

    df['data_origin'] = "scraped"
    return df

def compute_support_resistance(df, lookback=500, tolerance=0.005):
    support_levels = []
    resistance_levels = []

    for i in range(lookback, len(df)):
        range_slice = df[i-lookback:i]
        support = range_slice['low_price'].min()
        resistance = range_slice['high_price'].max()
        support_levels.append(support)
        resistance_levels.append(resistance)

    # Extend support and resistance levels to match dataframe length
    support_levels = [np.nan] * (lookback - 1) + support_levels
    resistance_levels = [np.nan] * (lookback - 1) + resistance_levels

    if len(support_levels) < len(df):
        support_levels.append(np.nan)
    if len(resistance_levels) < len(df):
        resistance_levels.append(np.nan)

    return support_levels, resistance_levels

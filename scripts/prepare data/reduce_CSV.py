import pandas as pd


file_path = '/home/martin/Documents/backtest/data/SPX_USD_2010_18_minute_ichimoku_EMA_DC.csv'
df = pd.read_csv(file_path)

df.tail(200000)

output_file = '/home/martin/Documents/backtest/data/reduced/reduced_SPX_USD_2010_18_minute_ichimoku_EMA_DC.csv'
df.to_csv(output_file, index=False)


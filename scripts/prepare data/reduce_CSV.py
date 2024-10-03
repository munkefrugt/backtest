import pandas as pd


file_path = '/home/martin/Documents/backtest/data/data_with_ichimoku.csv.csv'
df = pd.read_csv(file_path)

df.tail(100000)

output_file = '/home/martin/Documents/backtest/data/reduced_data_with_ichimoku.csv'
df.to_csv(output_file, index=False)


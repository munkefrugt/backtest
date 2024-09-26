import pandas as pd


file_path = 'data_with_ichimoku.csv'
df = pd.read_csv(file_path)

df.tail(30000)

output_file = 'reduced_data_with_ichimoku'
df.to_csv(output_file, index=False)


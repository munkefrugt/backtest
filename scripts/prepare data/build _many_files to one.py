import os
import pandas as pd

# Path to the folder containing CSV files
folder_path = '/home/martin/Documents/data/SPXUSD/'

# Initialize an empty list to store DataFrames
dfs = []

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):  # Only process CSV files
        file_path = os.path.join(folder_path, file_name)
        
        # Load each CSV file with the semicolon delimiter
        df = pd.read_csv(file_path, delimiter=';', header=None)
        
        # Manually assign column names since there's no header
        df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
        
        # Split 'datetime' into 'date' and 'time'
        df['date'] = df['datetime'].str.split().str[0]
        df['time'] = df['datetime'].str.split().str[1]
        
        # Combine 'date' and 'time' into a single 'datetime' column
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y%m%d %H%M%S')
        
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
merged_df = pd.concat(dfs)

# Set 'datetime' as the index
merged_df.set_index('datetime', inplace=True)

# Drop the redundant 'date' and 'time' columns
merged_df.drop(columns=['date', 'time'], inplace=True)

# Sort the DataFrame by the datetime index (in case the data is out of order)
merged_df.sort_index(inplace=True)

# Save the merged DataFrame to a CSV file
output_file_path = '/home/martin/Documents/data/SPXUSD/SPXUSD_2010_to_2018.csv'
merged_df.to_csv(output_file_path)

print(f'Merged file saved as: {output_file_path}')

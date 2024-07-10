import pandas as pd

# Path to the CSV file
csv_file = '2024-07-10.csv'

# Read the CSV file into a pandas DataFrame with 'Date' column parsed as datetime
df = pd.read_csv(csv_file, parse_dates=['Date'])

# Display the DataFrame
print(df)

import pandas as pd
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File path
file_path = os.path.join(BASE_DIR, 'data', 'sales_data.csv')

# Load dataset
df = pd.read_csv(file_path, encoding='latin1')

# Display first 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Display dataset info
print("\nDataset Information:")
print(df.info())

# Display missing values
print("\nMissing Values:")
print(df.isnull().sum())
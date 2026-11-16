import pandas as pd
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
input_file = os.path.join(BASE_DIR, 'data', 'sales_data.csv')
output_file = os.path.join(BASE_DIR, 'processed', 'cleaned_sales_data.csv')

# Load dataset
df = pd.read_csv(input_file, encoding='latin1')

print("Original Shape:", df.shape)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.fillna({
    'Postal Code': 0
}, inplace=True)

# Convert date
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Create Month-Year
df['Month_Year'] = df['Order Date'].dt.to_period('M')

# Create Total Sales
df['Total_Sales'] = df['Sales'] * df['Quantity']

print("\nCleaned Shape:", df.shape)

# Save cleaned data
df.to_csv(output_file, index=False)

print("\nCleaned data saved successfully!")
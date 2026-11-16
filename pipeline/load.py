import pandas as pd
from sqlalchemy import create_engine
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
input_file = os.path.join(BASE_DIR, 'processed', 'cleaned_sales_data.csv')
db_path = os.path.join(BASE_DIR, 'database', 'retail_sales.db')

# Load cleaned data
df = pd.read_csv(input_file)

# Database connection
engine = create_engine(f'sqlite:///{db_path}')

# Load into database
df.to_sql(
    name='sales_data',
    con=engine,
    if_exists='replace',
    index=False
)

print("Data loaded successfully into SQLite database!")
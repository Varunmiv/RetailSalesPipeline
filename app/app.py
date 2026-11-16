import io
import os

from flask import Flask, render_template, request, send_file
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

# Database connection
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, 'database', 'retail_sales.db')
engine = create_engine(f'sqlite:///{db_path}')

@app.route('/')
def dashboard():

    # Load data
    df = pd.read_sql('SELECT * FROM sales_data', engine)

    # Get selected category
    selected_category = request.args.get('category')

    # Apply filter if selected
    if selected_category and selected_category != "All":
        df = df[df['Category'] == selected_category]

    # Category List
    categories = df['Category'].unique().tolist()

    # KPI Calculations
    total_revenue = round(df['Total_Sales'].sum(), 2)
    total_orders = df['Order ID'].nunique()
    total_products = df['Product Name'].nunique()
    total_customers = df['Customer ID'].nunique()

    # Monthly Sales
    monthly_sales = df.groupby('Month_Year')['Total_Sales'].sum()

    months = monthly_sales.index.astype(str).tolist()
    sales = monthly_sales.values.tolist()

    # Top Products
    top_products = (
        df.groupby('Product Name')['Total_Sales']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    product_names = top_products.index.tolist()
    product_sales = top_products.values.tolist()

    # Category-wise Sales
    category_sales = (
        df.groupby('Category')['Total_Sales']
        .sum()
    )

    category_names = category_sales.index.tolist()
    category_values = category_sales.values.tolist()

        # Region-wise Sales
    region_sales = (
        df.groupby('Region')['Total_Sales']
        .sum()
    )

    region_names = region_sales.index.tolist()
    region_values = region_sales.values.tolist()

    return render_template(
        'dashboard.html',
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_products=total_products,
        total_customers=total_customers,
        months=months,
        sales=sales,
        product_names=product_names,
        product_sales=product_sales,
        category_names=category_names,
        category_values=category_values,
        categories=categories,
        selected_category=selected_category,
        region_names=region_names,
        region_values=region_values
    )


@app.route('/export')
def export_data():

    # Load data
    df = pd.read_sql('SELECT * FROM sales_data', engine)

    # Get selected category
    selected_category = request.args.get('category')

    # Apply filter
    if selected_category and selected_category != "All":
        df = df[df['Category'] == selected_category]

    # Export file (in-memory, avoids concurrent requests overwriting a shared file on disk)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='filtered_sales_data.csv'
    )


if __name__ == '__main__':
    app.run(debug=True)
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

def generate_data(records=1000):
    # Generate Base Sales Data
    sales_data = {
        'order_id': [f'ORD_{1000 + i}' for i in range(records)],
        'customer_id': [f'CUST_{random.randint(1, 200)}' for _ in range(records)],
        'order_date': [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) for _ in range(records)],
        'order_amount': np.round(np.random.uniform(20.0, 500.0, records), 2),
        'region': random.choices(['North', 'South', 'East', 'West'], k=records)
    }
    df_sales = pd.DataFrame(sales_data)

    # Generate Payment Gateway Data (with intentional errors)
    df_payments = df_sales.copy()
    
    # Introduce "The Leak": Remove 3% of records (Missing Payments)
    df_payments = df_payments.sample(frac=0.97)
    
    # Introduce "The Mismatch": Change amounts for 5% of records
    mismatch_idx = df_payments.sample(frac=0.05).index
    df_payments.loc[mismatch_idx, 'order_amount'] = df_payments.loc[mismatch_idx, 'order_amount'] * 0.9
    
    # Introduce "The Duplicate": Repeat 2% of records
    df_duplicates = df_payments.sample(frac=0.02)
    df_payments = pd.concat([df_payments, df_duplicates])

    # Save to CSV for your GitHub Repo
    df_sales.to_csv('raw_sales_data.csv', index=False)
    df_payments[['order_id', 'order_amount', 'order_date']].to_csv('payment_gateway_logs.csv', index=False)
    print("Success: 'raw_sales_data.csv' and 'payment_gateway_logs.csv' generated.")

if __name__ == "__main__":
    generate_data()
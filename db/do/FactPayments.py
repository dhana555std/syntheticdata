import random
from datetime import datetime, timedelta
from faker import Faker

def generate_FactPayments(FactOrders=None, DimPaymentMethod=None, DimDate=None, n=5000, seq_start=1):
    """
    Generates synthetic data for the FactPayments table.

    Args:
        FactOrders (list): A list of dictionaries representing rows from the FactOrders table.
        DimPaymentMethod (list): A list of dictionaries representing rows from the DimPaymentMethod table.
        DimDate (list): A list of dictionaries representing rows from the DimDate table.
        n (int): The number of rows to generate.
        seq_start (int): The starting value for the primary key sequence.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row.
    """
    fake = Faker()
    payments_data = []

    # Ensure dependency data is available
    if not FactOrders or not DimPaymentMethod or not DimDate:
         # In a real scenario, you might raise an error or return empty data
         # but assuming valid inputs based on prompt constraints for simplicity
         print("Warning: Dependency data (FactOrders, DimPaymentMethod, or DimDate) is missing or empty.")
         if not FactOrders:
             print("FactOrders is missing or empty.")
         if not DimPaymentMethod:
             print("DimPaymentMethod is missing or empty.")
         if not DimDate:
             print("DimDate is missing or empty.")
         if n > 0:
             print(f"Cannot generate {n} rows without valid dependency data. Returning empty list.")
         return []

    # Extract foreign key lists
    order_keys = [order['OrderKey'] for order in FactOrders if 'OrderKey' in order]
    payment_method_keys = [method['PaymentMethodKey'] for method in DimPaymentMethod if 'PaymentMethodKey' in method]
    date_keys = [date['DateKey'] for date in DimDate if 'DateKey' in date]

    # Ensure FK lists are not empty after extraction
    if not order_keys or not payment_method_keys or not date_keys:
         print("Warning: Could not extract necessary foreign keys from dependency data.")
         print(f"OrderKeys extracted: {len(order_keys)}")
         print(f"PaymentMethodKeys extracted: {len(payment_method_keys)}")
         print(f"DateKeys extracted: {len(date_keys)}")
         if n > 0:
             print(f"Cannot generate {n} rows without valid foreign keys. Returning empty list.")
         return []


    for i in range(n):
        payment_key = seq_start + i
        
        # Select random foreign keys
        order_key = random.choice(order_keys)
        payment_method_key = random.choice(payment_method_keys)
        date_key = random.choice(date_keys)

        # Generate amount (DECIMAL(10, 2))
        # Using pydecimal for better control over scale and precision
        amount = fake.pydecimal(left_digits=8, right_digits=2, positive=True)


        payments_data.append({
            "PaymentKey": payment_key,
            "OrderKey": order_key,
            "PaymentMethodKey": payment_method_key,
            "DateKey": date_key,
            "Amount": amount,
        })

    return payments_data

# Example Usage (assuming you have generated data for dependencies):
# from your_module import generate_FactOrders, generate_DimPaymentMethod, generate_DimDate
#
# # Generate dependency data first
# fact_orders_data = generate_FactOrders(...) # Pass necessary dependencies and params
# dim_payment_method_data = generate_DimPaymentMethod(...)
# dim_date_data = generate_DimDate(...)
#
# # Generate FactPayments data
# fact_payments_data = generate_FactPayments(
#     FactOrders=fact_orders_data,
#     DimPaymentMethod=dim_payment_method_data,
#     DimDate=dim_date_data,
#     n=100, # Generate 100 rows
#     seq_start=1001 # Start PK from 1001
# )
#
# # Print some generated data (optional)
# for i in range(min(5, len(fact_payments_data))):
#     print(fact_payments_data[i])

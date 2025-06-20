import random
from datetime import datetime, timedelta
from faker import Faker

def generate_FactPayments(FactOrders=None, DimPaymentMethod=None, DimDate=None, n=5000, seq_start=1):
    """
    Generates synthetic data for the FactPayments table.

    Args:
        FactOrders (list): A list of dictionaries containing FactOrders data, specifically OrderKey.
        DimPaymentMethod (list): A list of dictionaries containing DimPaymentMethod data, specifically PaymentMethodKey.
        DimDate (list): A list of dictionaries containing DimDate data, specifically DateKey.
        n (int): The number of rows to generate.
        seq_start (int): The starting value for the primary key sequence.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the FactPayments table.
    """
    fake = Faker()
    data = []

    # Extract foreign key lists, handling None or empty inputs
    order_keys = [order['OrderKey'] for order in FactOrders] if FactOrders else []
    payment_method_keys = [method['PaymentMethodKey'] for method in DimPaymentMethod] if DimPaymentMethod else []
    date_keys = [date['DateKey'] for date in DimDate] if DimDate else []

    # Check if foreign key data is available
    if not order_keys:
        print("Warning: No FactOrders data provided. Cannot generate FactPayments with valid OrderKeys.")
        # Decide how to handle: return empty list, or generate with placeholder/None?
        # Returning empty list for simplicity if FK data is missing.
        # Alternatively, you could generate with None or a default value if the schema allows.
        return []
    if not payment_method_keys:
         print("Warning: No DimPaymentMethod data provided. Cannot generate FactPayments with valid PaymentMethodKeys.")
         return []
    if not date_keys:
         print("Warning: No DimDate data provided. Cannot generate FactPayments with valid DateKeys.")
         return []

    for i in range(n):
        payment_key = seq_start + i

        row = {
            "PaymentKey": payment_key,
            "OrderKey": random.choice(order_keys), # Not unique
            "PaymentMethodKey": random.choice(payment_method_keys), # Not unique
            "DateKey": random.choice(date_keys), # Not unique
            "Amount": fake.pydecimal(left_digits=8, right_digits=2, positive=True, min_value=1, max_value=10000) # Not unique
        }
        data.append(row)

    return data

# Example Usage (requires having generated data for dependencies first)
# Assuming you have lists of dicts like:
# fact_orders_data = generate_FactOrders(...)
# dim_payment_method_data = generate_DimPaymentMethod(...)
# dim_date_data = generate_DimDate(...)
#
# fact_payments_data = generate_FactPayments(
#     FactOrders=fact_orders_data,
#     DimPaymentMethod=dim_payment_method_data,
#     DimDate=dim_date_data,
#     n=1000
# )
# print(len(fact_payments_data))
# print(fact_payments_data[0])

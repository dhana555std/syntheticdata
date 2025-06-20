import random
from datetime import datetime, timedelta
from faker import Faker

def generate_FactShipping(FactOrders=None, DimDate=None, n=5000, seq_start=1):
    fake = Faker()
    data = []

    # Extract foreign key values from dependency data
    order_keys = [order['OrderKey'] for order in FactOrders] if FactOrders else []
    date_keys = [date['DateKey'] for date in DimDate] if DimDate else []

    # Check if foreign key data is available
    if not order_keys:
        print("Warning: FactOrders dependency data is empty. Cannot generate valid OrderKey.")
        # Decide how to handle: skip generation, use None, or use placeholder
        # For this example, we'll continue but OrderKey will be None
        pass # order_keys remains empty

    if not date_keys:
        print("Warning: DimDate dependency data is empty. Cannot generate valid DateKeys.")
        # Decide how to handle: skip generation, use None, or use placeholder
        # For this example, we'll continue but DateKeys will be None
        pass # date_keys remains empty


    for i in range(n):
        shipping_key = seq_start + i

        # Pick random foreign keys if dependency data exists
        order_key = random.choice(order_keys) if order_keys else None
        shipping_date_key = random.choice(date_keys) if date_keys else None
        delivery_date_key = random.choice(date_keys) if date_keys else None # Simple random pick

        # Generate ShippingCost (DECIMAL(10, 2))
        shipping_cost = round(random.uniform(1.0, 200.0), 2) # Random cost between 1.00 and 200.00

        # Generate ShippingMethod (VARCHAR(100))
        shipping_method = fake.word() # Generates a single word, usually short

        # Ensure ShippingMethod does not exceed 100 characters (though fake.word() is likely short enough)
        if len(shipping_method) > 100:
             shipping_method = shipping_method[:100]


        row = {
            "ShippingKey": shipping_key,
            "OrderKey": order_key,
            "ShippingDateKey": shipping_date_key,
            "DeliveryDateKey": delivery_date_key,
            "ShippingCost": shipping_cost,
            "ShippingMethod": shipping_method,
        }
        data.append(row)

    return data

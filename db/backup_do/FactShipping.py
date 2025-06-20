import random
from datetime import datetime, timedelta
from faker import Faker
from decimal import Decimal

def generate_FactShipping(FactOrders=None, DimDate=None, n=5000, seq_start=1):
    fake = Faker()
    data = []

    # Prepare foreign key data
    if not FactOrders:
        # Handle empty or None dependency
        return []
    # Extract OrderKey values from the dependency data
    order_keys = [row['OrderKey'] for row in FactOrders]
    if not order_keys: # Also handle case where FactOrders is list but empty
         return []


    if not DimDate:
        # Handle empty or None dependency
        return []

    # Map DateKey to the actual date object for easier comparison
    # Assuming 'Date' column in DimDate is already a datetime object or date object
    date_map = {row['DateKey']: row['Date'] for row in DimDate}
    dim_date_rows = DimDate # Keep the list handy for filtering
    if not dim_date_rows: # Also handle case where DimDate is list but empty
        return []


    shipping_methods = ["Standard Shipping", "Express Shipping", "Next Day Delivery", "Same Day Delivery", "International Shipping"]

    for i in range(n):
        shipping_key = seq_start + i

        # Pick a random OrderKey from the available keys
        order_key = random.choice(order_keys)

        # Pick a random ShippingDateKey row and get the corresponding date object
        shipping_date_row = random.choice(dim_date_rows)
        shipping_date_key = shipping_date_row['DateKey']
        shipping_date = shipping_date_row['Date'] # This should be a datetime.date or datetime.datetime object

        # Find valid DeliveryDateKey rows (where date >= shipping_date)
        valid_delivery_date_rows = [
            row for row in dim_date_rows
            if row['Date'] >= shipping_date # Compare datetime objects directly
        ]

        # Pick a random DeliveryDateKey from the valid ones
        if valid_delivery_date_rows:
            delivery_date_row = random.choice(valid_delivery_date_rows)
            delivery_date_key = delivery_date_row['DateKey']
        else:
            # Fallback: If no date >= shipping_date exists (unlikely if DimDate is comprehensive), use the shipping date key
            # This could happen if DimDate only contains a single date
            delivery_date_key = shipping_date_key


        # Generate ShippingCost (DECIMAL(10, 2))
        # Ensure precision and scale
        shipping_cost = fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=1.00, max_value=1000.00)
        # Ensure it's a Decimal object
        # Using str() conversion is important for maintaining exact decimal value from pydecimal
        shipping_cost = Decimal(str(shipping_cost))


        # Generate ShippingMethod (VARCHAR(100))
        shipping_method = random.choice(shipping_methods)
        # The chosen methods are all <= 100 chars

        # Construct the row dictionary
        row = {
            "ShippingKey": shipping_key,
            "OrderKey": order_key,
            "ShippingDateKey": shipping_date_key,
            "DeliveryDateKey": delivery_date_key,
            "ShippingCost": shipping_cost,
            "ShippingMethod": shipping_method
        }
        data.append(row)

    return data

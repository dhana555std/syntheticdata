import random
from datetime import datetime
from faker import Faker

def generate_FactOrders(DimUser=None, DimProduct=None, DimDate=None, n=5000, seq_start=1):
    """
    Generates synthetic data for the FactOrders table.

    Args:
        DimUser (list of dict, optional): List of dictionaries containing UserKey values from DimUser.
        DimProduct (list of dict, optional): List of dictionaries containing ProductKey values from DimProduct.
        DimDate (list of dict, optional): List of dictionaries containing DateKey values from DimDate.
        n (int): The number of rows to generate.
        seq_start (int): The starting value for the primary key (OrderKey).

    Returns:
        list: A list of dictionaries, each representing a row in the FactOrders table.
    """
    fake = Faker()
    data = []

    if not DimUser or not DimProduct or not DimDate:
        print("Dependency data (DimUser, DimProduct, or DimDate) is missing or empty.")
        print("Cannot generate FactOrders data without valid foreign keys.")
        return []

    # Extract foreign key lists for efficient random selection
    user_keys = [row['UserKey'] for row in DimUser if 'UserKey' in row]
    product_keys = [row['ProductKey'] for row in DimProduct if 'ProductKey' in row]
    date_keys = [row['DateKey'] for row in DimDate if 'DateKey' in row]

    if not user_keys or not product_keys or not date_keys:
         print("Could not extract foreign keys from dependency data.")
         return []

    for i in range(n):
        order_key = seq_start + i
        user_key = random.choice(user_keys)
        product_key = random.choice(product_keys)
        date_key = random.choice(date_keys)

        # Generate Quantity (random integer, e.g., 1 to 50)
        quantity = random.randint(1, 50)

        # Generate Price (random decimal between 5.00 and 500.00 with 2 decimal places)
        # Using pydecimal for better control over decimal values
        price = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        # Ensure price is within a reasonable range if pydecimal generates out of typical bounds
        price = max(5.00, min(500.00, price))


        # Calculate TotalAmount = Quantity * Price, rounded to 2 decimal places
        total_amount = round(quantity * price, 2)

        row = {
            "OrderKey": order_key,
            "UserKey": user_key,
            "ProductKey": product_key,
            "DateKey": date_key,
            "Quantity": quantity,
            "Price": price,
            "TotalAmount": total_amount
        }
        data.append(row)

    return data

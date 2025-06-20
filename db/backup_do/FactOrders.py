import random
from datetime import datetime, timedelta
from faker import Faker

def generate_FactOrders(DimUser=None, DimProduct=None, DimDate=None, n=5000, seq_start=1):
    """
    Generates synthetic data for the FactOrders table.

    Args:
        DimUser: List of dictionaries representing rows from the DimUser table.
                 Used for foreign key lookups.
        DimProduct: List of dictionaries representing rows from the DimProduct table.
                    Used for foreign key lookups.
        DimDate: List of dictionaries representing rows from the DimDate table.
                 Used for foreign key lookups.
        n (int): The number of rows to generate.
        seq_start (int): The starting value for the primary key sequence.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row
              in the FactOrders table.
    """
    fake = Faker()
    data = []

    if n <= 0:
        return data

    # Extract foreign key lists
    user_keys = [user['UserKey'] for user in DimUser] if DimUser else []
    product_keys = [product['ProductKey'] for product in DimProduct] if DimProduct else []
    date_keys = [date['DateKey'] for date in DimDate] if DimDate else []

    # Check if foreign key lists are empty if n > 0
    if n > 0 and (not user_keys or not product_keys or not date_keys):
         # Depending on requirements, could raise error or return empty.
         # Returning empty as a safe default if dependencies are missing.
         # In a real scenario, FK columns are NOT NULL, so missing dependencies
         # for n > 0 rows would be an issue.
         if not user_keys:
             print("Warning: DimUser dependency is empty. Cannot generate FactOrders.")
         if not product_keys:
             print("Warning: DimProduct dependency is empty. Cannot generate FactOrders.")
         if not date_keys:
             print("Warning: DimDate dependency is empty. Cannot generate FactOrders.")
         return []


    for i in range(n):
        order_key = seq_start + i

        # Select random foreign keys from the provided lists
        user_key = random.choice(user_keys)
        product_key = random.choice(product_keys)
        date_key = random.choice(date_keys)

        # Generate other data
        quantity = fake.random_int(min=1, max=100) # Example range for quantity
        price = fake.pydecimal(left_digits=8, right_digits=2, positive=True) # Example for price
        total_amount = fake.pydecimal(left_digits=8, right_digits=2, positive=True) # Example for total_amount


        row = {
            "OrderKey": order_key,
            "UserKey": user_key,
            "ProductKey": product_key,
            "DateKey": date_key,
            "Quantity": quantity,
            "Price": price,
            "TotalAmount": total_amount,
        }
        data.append(row)

    return data


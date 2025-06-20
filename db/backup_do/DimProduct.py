import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimProduct(n=5000, seq_start=1):
    """
    Generates synthetic data for the DimProduct table.

    Args:
        n (int): The number of rows to generate.
        seq_start (int): The starting value for the primary key sequence.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row.
    """
    fake = Faker()
    data = []

    # Specific lists for less variety or more realistic data if needed
    product_categories = ['Electronics', 'Clothing', 'Home Goods', 'Books', 'Toys', 'Sports', 'Groceries', 'Beauty', 'Automotive']

    for i in range(n):
        product_key = seq_start + i
        
        # Generate data according to constraints and descriptions
        product_id = fake.random_int(min=1000, max=99999) # Not unique
        
        # Name - VARCHAR(255), not unique
        # Using fake.word() or a combination to ensure length limit
        name = fake.word() + " " + fake.catch_phrase()
        name = name[:255].strip() # Truncate if necessary

        # CategoryName - VARCHAR(100), not unique
        category_name = random.choice(product_categories)

        # SKU - VARCHAR(50), specific format using sequence
        sku = f"sku_{product_key}@sku.com"
        
        data.append({
            "ProductKey": product_key,
            "ProductID": product_id,
            "Name": name,
            "CategoryName": category_name,
            "SKU": sku
        })

    return data


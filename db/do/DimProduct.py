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
        list: A list of dictionaries, each representing a row in the DimProduct table.
    """
    fake = Faker()
    data = []

    for i in range(n):
        product_key = seq_start + i
        
        # Constraints based on extra_info and DDL
        product_id = fake.random_int(min=1000, max=9999) # "This is not unique"
        name = fake.word() # "This is not unique"
        category_name = fake.word() # "This is not unique"
        sku = f"sku_{product_key}@sku.com" # "If SKU, use sku_{seq_start}@sku.com"

        # Ensure VARCHAR lengths are respected
        name = name[:255]
        category_name = category_name[:100]
        sku = sku[:50]

        row = {
            "ProductKey": product_key,
            "ProductID": product_id,
            "Name": name,
            "CategoryName": category_name,
            "SKU": sku
        }
        data.append(row)

    return data

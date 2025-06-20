import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimCategory(n=5000, seq_start=1):
    fake = Faker()
    data = []
    for i in range(n):
        category_key = seq_start + i
        category_id = random.randint(1, 100) # Generate a non-unique integer ID
        category_name = fake.word() # Generate a non-unique word
        description = fake.text() # Generate text description

        data.append({
            "CategoryKey": category_key,
            "CategoryID": category_id,
            "CategoryName": category_name,
            "Description": description
        })
    return data

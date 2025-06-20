import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimCategory(n=5000, seq_start=1):
    fake = Faker()
    data = []
    for i in range(n):
        category_key = seq_start + i
        
        # CategoryID: INT, not unique
        category_id = fake.random_int(min=1, max=100) # Example range

        # CategoryName: VARCHAR(100), not unique
        # fake.word() or fake.sentence() sliced can work. word() is safer for length.
        category_name = fake.word()

        # Description: TEXT, not unique
        description = fake.text(max_nb_chars=300) # Generate a description text

        data.append({
            "CategoryKey": category_key,
            "CategoryID": category_id,
            "CategoryName": category_name,
            "Description": description
        })
    return data

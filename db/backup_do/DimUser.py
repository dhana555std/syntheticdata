import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimUser(n=5000, seq_start=1):
    fake = Faker()
    data = []
    for i in range(n):
        user_key = seq_start + i
        
        # UserID: Not unique, generate a random integer
        user_id = fake.random_int(min=1000, max=99999)
        
        # Name: Use fake.name()
        name = fake.name()
        
        # Email: Use format user_{seq_start}@gmail.com
        email = f"user_{user_key}@gmail.com"
        
        # Role: Not unique, use fake.word() or select from a list
        role = fake.word() # Could use fake.job() or a predefined list if roles were specific

        data.append({
            "UserKey": user_key,
            "UserID": user_id,
            "Name": name,
            "Email": email,
            "Role": role
        })
    return data

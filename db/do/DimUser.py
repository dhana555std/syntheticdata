import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimUser(n=5000, seq_start=1):
    fake = Faker()
    data = []
    roles = ['Admin', 'User', 'Guest', 'Moderator']

    for i in range(n):
        user_key = seq_start + i
        user_id = random.randint(1000, 99999) # Assuming UserID is just an identifier, not necessarily unique
        name = fake.name()
        email = f"user_{user_key}@gmail.com"
        role = random.choice(roles)

        row = {
            "UserKey": user_key,
            "UserID": user_id,
            "Name": name,
            "Email": email,
            "Role": role
        }
        data.append(row)

    return data

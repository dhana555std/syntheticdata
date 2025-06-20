import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimShipping(n=5000, seq_start=1):
    fake = Faker()
    data = []
    for i in range(n):
        shipping_key = seq_start + i
        carrier = fake.company()[:50] # VARCHAR(50)
        country = fake.country()[:100] # VARCHAR(100)
        city = fake.city()[:100] # VARCHAR(100)
        state = fake.state()[:100] # VARCHAR(100)
        postal_code = fake.postcode()[:20] # VARCHAR(20)

        data.append({
            "ShippingKey": shipping_key,
            "Carrier": carrier,
            "Country": country,
            "City": city,
            "State": state,
            "PostalCode": postal_code,
        })
    return data

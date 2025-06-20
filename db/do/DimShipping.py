import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimShipping(n=5000, seq_start=1):
    fake = Faker()
    data = []
    for i in range(n):
        shipping_key = seq_start + i
        carrier = fake.company()
        country = fake.country()
        city = fake.city()
        state = fake.state()
        postal_code = fake.postcode()

        data.append({
            "ShippingKey": shipping_key,
            "Carrier": carrier,
            "Country": country,
            "City": city,
            "State": state,
            "PostalCode": postal_code
        })
    return data

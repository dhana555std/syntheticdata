import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimPaymentMethod(n=5000, seq_start=1):
    fake = Faker()
    data = []

    # Define a list of common payment methods
    payment_methods = [
        'Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash',
        'Check', 'Gift Card', 'Mobile Payment', 'Cryptocurrency', 'Wire Transfer',
        'Online Transfer', 'Direct Debit', 'Invoice', 'Store Credit'
    ]

    for i in range(n):
        row = {}

        # PaymentMethodKey: Primary key, auto increment, use seq_start
        row['PaymentMethodKey'] = seq_start + i

        # Method: VARCHAR(50), not unique
        # Select a random method from the predefined list
        row['Method'] = random.choice(payment_methods)

        data.append(row)

    return data

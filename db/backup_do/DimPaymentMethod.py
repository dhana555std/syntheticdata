import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimPaymentMethod(n=5000, seq_start=1):
    fake = Faker()
    data = []

    for i in range(n):
        payment_method_key = seq_start + i
        
        # Generate Method: VARCHAR(50), not unique
        # Choose from common payment methods or generate a word/phrase
        method_options = [
            "Credit Card", "Debit Card", "PayPal", "Bank Transfer", 
            "Cash", "Cheque", "Mobile Payment", "Gift Card"
        ]
        method = random.choice(method_options)
        
        # Ensure method length is within VARCHAR(50) limit
        if len(method) > 50:
             method = method[:50] # Truncate if necessary, though unlikely with common options

        row = {
            "PaymentMethodKey": payment_method_key,
            "Method": method
        }
        data.append(row)

    return data

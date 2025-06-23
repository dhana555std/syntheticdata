import csv
import datetime
import random
import os
from faker import Faker

# Configuration
NUM_RECORDS = 5000
OUTPUT_DIR = "./generated_csv_data/"
OUTPUT_FILENAME = "all_data_2025-06-23_19-26-57.csv"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

# Initialize Faker
fake = Faker()

# Define column headers based on the sample data
headers = [
    "user_id",
    "account_balance",
    "is_active",
    "customer_uuid",
    "signup_date",
    "profile_text",
    "first_name",
    "email_address",
    "personal_website",
    "contact_number",
    "order_status",
    "rating",
    "currency_code",
    "postal_code",
    "country",
    "state",
    "city",
    "notes",
]

# Define possible values for categorical columns based on the sample
order_statuses = ["completed", "pending", "shipped", "processing", "cancelled"]
ratings = [3, 4, 5]
currency_codes = ["USD", "JPY", "EUR", "AUD", "GBP", "CAD"]

# Define date range for signup_date based on sample (roughly 2022-2024)
start_date = datetime.datetime(2022, 1, 1)
end_date = datetime.datetime(2024, 12, 31)


# Function to generate a single synthetic record
def generate_record():
    return {
        "user_id": random.randint(100, 200),  # Based on sample range
        "account_balance": round(random.uniform(1000, 10000), 2),  # Float with 2 decimals
        "is_active": random.choice([True, False]),  # Boolean
        "customer_uuid": fake.bothify(text="sdv-id-######"),  # Alphanumeric with prefix
        "signup_date": fake.date_time_between(
            start_date=start_date, end_date=end_date
        ).strftime("%Y-%m-%d %H:%M:%S"),  # Datetime string
        "profile_text": fake.sentence(nb_words=random.randint(5, 10)),  # Sentence
        "first_name": fake.first_name(),  # First name
        "email_address": fake.email(),  # Email
        "personal_website": fake.url(),  # URL
        "contact_number": fake.phone_number(),  # Phone number
        "order_status": random.choice(order_statuses),  # Categorical
        "rating": random.choice(ratings),  # Categorical integer
        "currency_code": random.choice(currency_codes),  # Categorical
        "postal_code": fake.zipcode(),  # Postal code (string)
        "country": fake.country(),  # Country name
        "state": fake.state(),  # State name
        "city": fake.city(),  # City name
        "notes": fake.sentence(nb_words=random.randint(5, 10)),  # Sentence
    }


# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate and save data to CSV
with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)

    writer.writeheader()
    for _ in range(NUM_RECORDS):
        writer.writerow(generate_record())

# Print the output file path
print(OUTPUT_PATH)
import csv
import os
import random
import datetime
from faker import Faker

# Configuration
NUM_RECORDS = 5000
OUTPUT_DIR = './generated_csv_data/'
OUTPUT_FILENAME = 'all_data_2025-06-20_15-29-16.csv'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

# Initialize Faker
fake = Faker()

# Define observed enums and ranges from the sample data
profile_texts = [
    "Feedback provider, helps improve services",
    "Active community member",
    "Long-term subscriber, rarely contacts support",
    "New user exploring features",
    "Loyal customer with frequent purchases",
    "Interested in new product releases",
]

order_statuses = [
    "completed",
    "pending",
    "shipped",
    "processing",
    "cancelled",
]

ratings = [3, 4, 5]

currency_codes = [
    "USD",
    "JPY",
    "EUR",
    "AUD",
    "GBP",
    "CAD",
]

countries = [
    "United Kingdom",
    "Japan",
    "Australia",
    "Germany",
    "Canada",
    "United States",
]

notes = [
    "Customer since 2023",
    "VIP customer, provide priority support",
    "No specific preferences",
    "Follow up on recent inquiry",
    "Preferred contact time: mornings",
    "Interested in new features",
    "Has expressed interest in premium plan",
]

user_id_range = (123, 136) # Observed range

# Define the date range based on sample data
start_date = datetime.datetime(2022, 5, 10)
end_date = datetime.datetime(2024, 3, 3)

# Define the CSV header
header = [
    'user_id',
    'account_balance',
    'is_active',
    'customer_uuid',
    'signup_date',
    'profile_text',
    'first_name',
    'email_address',
    'personal_website',
    'contact_number',
    'order_status',
    'rating',
    'currency_code',
    'postal_code',
    'country',
    'state',
    'city',
    'notes',
]

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate synthetic data
data = []
for _ in range(NUM_RECORDS):
    record = {
        'user_id': random.randint(user_id_range[0], user_id_range[1]),
        'account_balance': round(random.uniform(1000.00, 10000.00), 2), # Using random.uniform for a wider range than sample, rounded
        'is_active': fake.pybool(),
        'customer_uuid': fake.bothify(text='sdv-id-??????'), # sdv-id- + 6 alphanumeric chars
        'signup_date': fake.date_time_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d %H:%M:%S'),
        'profile_text': random.choice(profile_texts),
        'first_name': fake.first_name(),
        'email_address': fake.email(),
        'personal_website': fake.url(),
        'contact_number': fake.phone_number(),
        'order_status': random.choice(order_statuses),
        'rating': random.choice(ratings),
        'currency_code': random.choice(currency_codes),
        'postal_code': fake.bothify('#####'), # 5 digits
        'country': random.choice(countries),
        'state': fake.state(), # Generates US states by default, consistent with sample states
        'city': fake.city(),
        'notes': random.choice(notes),
    }
    data.append(record)

# Save data to CSV
with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)

    writer.writeheader()
    writer.writerows(data)

# Print the output file path
print(OUTPUT_PATH)

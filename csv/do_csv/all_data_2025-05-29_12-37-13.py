import csv
import os
import io
import random
import datetime
from faker import Faker

# Reference CSV data provided as a string
csv_data = """user_id,account_balance,is_active,customer_uuid,signup_date,profile_text,first_name,email_address,personal_website,contact_number,order_status,rating,currency_code,postal_code,country,state,city,notes
136,6699.02,True,sdv-id-QcBdOV,2022-05-10 18:57:00,"Feedback provider, helps improve services",Michael,lesliebradford@example.org,https://www.diana34.com,+1-404-777-5678,completed,5,USD,13294.0,,New Hampshire,West Jerry,Customer since 2023
124,1662.45,False,sdv-id-tUGmPo,2022-05-23 03:12:04,Active community member,Michael,kanderson@example.org,https://www.karen89.com,+1-717-999-0123,completed,5,JPY,83355.0,United Kingdom,Vermont,New John,"VIP customer, provide priority support"
124,4746.31,True,sdv-id-pNfCtx,2022-05-31 07:09:10,Active community member,Ashley,blackmark@example.org,https://www.bob78.com,+1-909-333-6789,completed,4,USD,84705.0,Japan,New Hampshire,New Kylietown,No specific preferences
128,9768.49,False,sdv-id-yaqNmY,2023-02-21 08:09:56,Active community member,Regina,daughertyjesse@example.org,https://www.diana34.com,+1-212-444-0123,pending,3,EUR,4032.0,United Kingdom,Kentucky,Charleston,Follow up on recent inquiry
129,8255.72,False,sdv-id-VznfnD,2022-05-30 13:02:17,Active community member,Carrie,leejoseph@example.org,https://alice.com,+1-212-444-0123,pending,5,JPY,25302.0,Australia,Maine,Brooksberg,Preferred contact time: mornings
133,1828.91,True,sdv-id-aesTGx,2023-05-10 21:46:54,"Feedback provider, helps improve services",Jacob,angela68@example.com,https://alice.com,+1-606-999-3456,shipped,5,AUD,72438.0,Germany,Virginia,Sydneyhaven,No specific preferences
126,7615.12,False,sdv-id-qhhdGD,2024-02-02 13:00:33,"Long-term subscriber, rarely contacts support",Melissa,danaallen@example.net,https://www.diana34.com,+1-717-999-0123,pending,5,GBP,47910.0,Canada,South Carolina,Rodriguezburgh,No specific preferences
123,9867.64,True,sdv-id-wzczIE,2022-12-04 22:22:59,"Feedback provider, helps improve services",Melissa,zaguilar@example.net,https://www.diana34.com,+1-717-999-0123,pending,5,JPY,99105.0,United Kingdom,Louisiana,Lake Williamton,No specific preferences
124,7425.92,False,sdv-id-SueJyZ,2023-01-21 12:41:26,"Feedback provider, helps improve services",Jeffrey,chavezdavid@example.org,https://www.ivy45.com,+1-717-999-0123,pending,5,CAD,54748.0,United States,Wisconsin,Carrietown,Has expressed interest in premium plan
125,1235.95,False,sdv-id-EaQOuG,2023-10-28 13:17:51,Loyal customer with frequent purchases,Elizabeth,victor19@example.org,https://www.jack67.com,+1-717-999-0123,pending,5,CAD,68134.0,Canada,Mississippi,New Christopherland,"VIP customer, provide priority support"
133,5128.06,False,sdv-id-ZcqiRj,2022-11-18 08:34:28,New user exploring features,Angel,smeyers@example.org,https://www.karen89.com,+1-808-222-2345,processing,3,CAD,30762.0,Germany,New Hampshire,Port Rebeccaborough,Interested in new features
131,6634.29,True,sdv-id-oxPIQL,2024-03-03 17:59:32,Active community member,Stephen,greenwendy@example.org,https://www.bob78.com,+1-515-777-2345,cancelled,5,AUD,51136.0,Japan,South Dakota,South Edward,"VIP customer, provide priority support"
133,5313.31,True,sdv-id-bktakn,2022-06-13 11:28:01,New user exploring features,Emily,jyoung@example.com,https://www.karen89.com,+1-202-555-0123,pending,5,JPY,58879.0,Canada,Texas,Skinnerview,Interested in new features
125,9426.28,False,sdv-id-dhJSYJ,2023-01-18 17:12:49,Interested in new product releases,Chloe,lisa32@example.net,https://www.bob78.com,+1-313-555-4567,pending,5,CAD,54328.0,Canada,Mississippi,Joshualand,No specific preferences
"""

# Read the reference data to infer columns and value pools
csvfile = io.StringIO(csv_data)
reader = csv.reader(csvfile)
header = next(reader)
reference_rows = list(reader)

# --- Inference ---
inferred_pools = {col: set() for col in header}
for row in reference_rows:
    for i, value in enumerate(row):
        inferred_pools[header[i]].add(value)

# Convert sets to lists for random choice
for col in inferred_pools:
    inferred_pools[col] = list(inferred_pools[col])

# Define Faker mappings based on inference and observed patterns
fake = Faker()

def generate_record(header, inferred_pools, fake):
    record = {}
    for col in header:
        if col == 'user_id':
            # Inferred int, range observed 123-136, use a slightly wider range
            record[col] = fake.random_int(min=100, max=200)
        elif col == 'account_balance':
            # Inferred float with 2 decimal places
            record[col] = round(random.uniform(100.0, 10000.0), 2)
        elif col == 'is_active':
            # Inferred boolean
            record[col] = fake.boolean()
        elif col == 'customer_uuid':
            # Inferred pattern sdv-id-XXXXXX
            record[col] = fake.bothify(text='sdv-id-??????')
        elif col == 'signup_date':
            # Inferred datetime format YYYY-MM-DD HH:MM:SS
            # Generate dates within a reasonable past range
            record[col] = fake.date_time_between(start_date='-3y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        elif col == 'profile_text':
            # Inferred enum/limited options, allow empty string sometimes
            if random.random() < 0.1: # 10% chance of empty
                 record[col] = ""
            else:
                record[col] = random.choice(inferred_pools.get(col, [fake.sentence()])) # Use pool if available, else sentence
        elif col == 'first_name':
            record[col] = fake.first_name()
        elif col == 'email_address':
            record[col] = fake.email()
        elif col == 'personal_website':
            # Inferred URL, sometimes from sample pool, sometimes general URL, allow empty
            if random.random() < 0.1: # 10% chance of empty
                record[col] = ""
            elif random.random() < 0.3: # 30% chance of picking from sample pool
                 # Filter out empty strings from the pool before choosing
                 valid_pool = [url for url in inferred_pools.get(col, []) if url]
                 if valid_pool:
                      record[col] = random.choice(valid_pool)
                 else:
                      record[col] = fake.url()
            else:
                record[col] = fake.url()
        elif col == 'contact_number':
            # Inferred pattern +1-XXX-XXX-XXXX
            record[col] = fake.bothify(text='+1-###-###-####')
        elif col == 'order_status':
             # Inferred enum
            record[col] = random.choice(inferred_pools.get(col, ['completed', 'pending', 'shipped', 'cancelled'])) # Use pool if available, else default list
        elif col == 'rating':
            # Inferred enum/limited int
             # Filter out empty strings from the pool and convert to int
             valid_pool = [int(r) for r in inferred_pools.get(col, []) if r.isdigit()]
             if not valid_pool: valid_pool = [3, 4, 5] # Default if pool is empty
             record[col] = random.choice(valid_pool)
        elif col == 'currency_code':
            # Inferred enum
            record[col] = random.choice(inferred_pools.get(col, ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'])) # Use pool if available, else default list
        elif col == 'postal_code':
            # Inferred string/number, can be empty. Ignore the .0 suffix from sample.
            if random.random() < 0.15: # 15% chance of empty
                record[col] = ""
            else:
                record[col] = fake.zipcode() # Generates a string suitable for postal code
        elif col == 'country':
            # Inferred string, can be empty
            if random.random() < 0.2: # 20% chance of empty
                record[col] = ""
            else:
                record[col] = fake.country()
        elif col == 'state':
            # Inferred string, can be empty
            if random.random() < 0.2: # 20% chance of empty
                record[col] = ""
            else:
                record[col] = fake.state()
        elif col == 'city':
            # Inferred string, can be empty
            if random.random() < 0.2: # 20% chance of empty
                record[col] = ""
            else:
                record[col] = fake.city()
        elif col == 'notes':
             # Inferred enum/limited options, can be empty
            if random.random() < 0.25: # 25% chance of empty
                 record[col] = ""
            else:
                # Filter out empty strings from the pool before choosing
                valid_pool = [note for note in inferred_pools.get(col, []) if note]
                if valid_pool:
                     record[col] = random.choice(valid_pool)
                else:
                     record[col] = fake.sentence() # Default if pool is empty or contains only empty strings
        else:
            # Default case for any unhandled columns
            record[col] = fake.word()

    return [record[col] for col in header]

# --- Data Generation ---
num_records = 5000
generated_data = []

for _ in range(num_records):
    generated_data.append(generate_record(header, inferred_pools, fake))

# --- Save to CSV ---
output_dir = './generated_csv_data/'
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
output_filename = f'all_data_{timestamp}.csv'
output_filepath = os.path.join(output_dir, output_filename)

with open(output_filepath, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)
    writer.writerows(generated_data)

print(output_filepath)

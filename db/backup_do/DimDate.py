import random
from datetime import datetime, timedelta, date
from faker import Faker

def generate_DimDate(n=5000, seq_start=1):
    """
    Generates synthetic data for the DimDate table.

    Args:
        n (int): The number of rows to generate.
        seq_start (int): The starting sequence number for the primary key DateKey.

    Returns:
        list: A list of dictionaries, each representing a row in the DimDate table.
    """
    fake = Faker()
    data = []

    # Define a reasonable date range for the dimension table
    start_date = date(2020, 1, 1)
    end_date = date(2025, 12, 31)
    
    # Generate dates sequentially or randomly within the range?
    # A date dimension table usually has consecutive dates.
    # Let's generate 'n' consecutive dates starting from start_date.
    # If n is larger than the number of days in the range, we will exceed the range.
    # Let's cap the number of days generated or pick randomly within the range.
    # Given the structure, generating 'n' distinct date objects seems more appropriate
    # rather than strictly consecutive days, unless specified.
    # Let's generate random dates within the range.

    generated_dates = set() # To ensure unique dates if needed, though not required by PK on DateKey
    
    for i in range(n):
        date_key = seq_start + i
        
        # Generate a random date object within the defined range
        # Faker's date_between takes date objects or strings
        random_date_obj = fake.date_between(start_date=start_date, end_date=end_date)

        # Derive other date parts from the date object
        date_value = random_date_obj.strftime('%Y-%m-%d') # Format as YYYY-MM-DD string
        day = random_date_obj.day
        month = random_date_obj.month
        year = random_date_obj.year
        quarter = (random_date_obj.month - 1) // 3 + 1
        week = random_date_obj.isocalendar()[1] # ISO week number
        day_of_week = random_date_obj.isocalendar()[2] # ISO weekday (Monday=1, Sunday=7)

        row = {
            "DateKey": date_key,
            "Date": date_value,
            "Day": day,
            "Month": month,
            "Year": year,
            "Quarter": quarter,
            "Week": week,
            "DayOfWeek": day_of_week,
        }
        data.append(row)

    return data

# Note: The function is defined above. No main execution block is included as per requirements.

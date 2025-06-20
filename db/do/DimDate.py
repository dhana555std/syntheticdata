import random
from datetime import datetime, timedelta
from faker import Faker

def generate_DimDate(n=5000, seq_start=1):
    """
    Generates synthetic data for the DimDate table.

    Args:
        n (int): The number of rows to generate.
        seq_start (int): The starting value for the primary key sequence.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row.
    """
    fake = Faker()
    data = []

    # Generate dates within a reasonable range, e.g., last 10 years
    start_date = datetime.now() - timedelta(days=10*365)
    end_date = datetime.now()

    # To ensure variety and cover different days/months/years
    # we can generate dates sequentially starting from a past date
    # or just generate random dates within a range.
    # Given the structure, generating dates sequentially seems more aligned
    # with a typical date dimension table, where DateKey increments with Date.
    # Let's generate dates sequentially starting from a fixed date.

    # Let's start from 2020-01-01 as an example fixed date
    current_date = datetime(2020, 1, 1)
    
    for i in range(n):
        date_key = seq_start + i
        
        # Generate a date object
        # For a typical DimDate, we would generate sequential dates.
        # If n is large, we might need to adjust the start date or method.
        # Let's use sequential dates for now.
        current_date_obj = current_date + timedelta(days=i)

        # Extract components
        date_str = current_date_obj.strftime("%Y-%m-%d")
        day = current_date_obj.day
        month = current_date_obj.month
        year = current_date_obj.year
        quarter = (month - 1) // 3 + 1
        week = current_date_obj.isocalendar()[1] # ISO week number (1-53)
        day_of_week = current_date_obj.isoweekday() # Monday=1, Sunday=7

        row = {
            "DateKey": date_key,
            "Date": date_str,
            "Day": day,
            "Month": month,
            "Year": year,
            "Quarter": quarter,
            "Week": week,
            "DayOfWeek": day_of_week,
        }
        data.append(row)

    return data


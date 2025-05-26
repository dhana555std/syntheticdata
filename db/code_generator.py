import json
import re

from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from utils.llm_utils import get_llm

llm = get_llm()
output_parser = StrOutputParser()

PROMPT = PromptTemplate.from_template("""
You are a Python code generator specialized in creating synthetic data using the Faker library.

Your task:
Generate a complete Python function named generate_{table} that produces synthetic data for 
a single database table, respecting constraints and dependencies.
Inputs:
1. ddl (string): The full CREATE TABLE SQL statement for the target table:
{ddl}

2. dependencies (list of dependency table names): The following are passed as lists of dicts representing
foreign key values: {dependencies}
{tables_str}
- If column description says NOT UNIQUE then do not add constraints like fake.unique.*.
  Example : "CategoryName": "Name of the category max length = 100 NOT UNIQUE"
Requirements for generated code:
- Do not generate main method (if __name__ == '__main__':) at all not needed.
- If there is no constraint to uuid as primary key use seq_start.
- The function signature should be:
  def generate_{table}({dependencies},n=5000, seq_start=1): maintain the order of arguments from dependency graph.
  if the dependencies is empty string then generate:- def generate_{table}(n=5000, seq_start=1)
- If primary key is uuid then use uuid else use use seq_start as primary key and keep increamenting with i.
- if PRIMARY key have CategoryID CHAR(36) PRIMARY KEY AUTO_INCREMENT, then use the UUID as the primary key instead of the seq_start.
  Example : CategoryID = fake.uuid4()
- Maintain referential integrity between tables.
- Use Faker, random, and datetime to generate realistic data.
- Use Faker, random, datetime, and timedelta from Python standard library.
- NEVER use `faker.timedelta`. It does not exist.
- To generate a datetime after another datetime (e.g., for last_updated_time after creation_time), use:
  faker.date_time_between_dates(datetime_start=creation_time, datetime_end=datetime.now())
- ALWAYS format datetime values using:
  dt.strftime("%Y-%m-%d %H:%M:%S") + ".000"
  Use formatting only when storing in the final dictionary using:
- Do NOT format datetime too early if it needs to be passed to Faker or compared with another datetime.
- Only format datetime values to string *after* all datetime operations are complete.
- Respect constraints (PRIMARY KEY, NOT NULL, UNIQUE, FOREIGN KEY).
- Use dependency tables for foreign keys.
- Handle audit/meta columns (created_by, updated_by, creation_time, updating_time) with sensible fake data.
- Parse and apply the extra_info text instructions for column data generation.
- Include all necessary imports at the top of the code.
  Example: 
          - import random
          - from datetime import datetime, timedelta
          - from faker import Faker
- Return a list of dictionaries representing rows.
- Output only the Python code (no comments or explanation).
- For creation_time and updating_time use 
- For date time the format should able get parsed with json                                      
- For UNIQUE column values use appending suffix like numbers +i to maintain uniqueness
- Add None and a default value for all the arguments.
- ⚠️ Never pass a formatted string (like "2025-01-14 09:33:50.000") as input to Faker datetime functions.
  Always keep values as datetime objects until final assignment into the dictionary.
dt = faker.date_time_this_year(before_now=True)                  
# Format as required
formatted = dt.strftime("%Y-%m-%d %H:%M:%S") + ".000"

Example 1 : if in dependencies roles → [] there is no any dependency generate function structure like this
            def generate_roles(n=5000):
                        
Example 2 : if in dependencies inventory → ['products', 'warehouses'] there are two dependencies then generate function structure like this
            def generate_inventory(warehouses, products, n=5000):
                                    
Example 3 : if in function structure there is created_by_data or updated_by_data generate function structure like this
            def function_name(created_by_data=None, updated_by_data=None, n=5000):
                                     
Example 4: Faker should respect schema constraints on data length.
For example, session_id CHAR(36) allows a maximum of 36 characters, so Faker must generate a value no longer than 36 characters
""")


def generate_code(table, ddl, dependencies, tables_str):
    
    print(f"before table string is : {tables_str}")
    tables_str = str(tables_str)
    if tables_str and tables_str.strip() != "":
      tables_str = "Consider the following constraints for generating column data:\n" + tables_str

    print(f"after table string is : {tables_str}")

    

    """
    """
    try:
        chain = PROMPT | llm | StrOutputParser()
        print(f"prompt is {PROMPT}")

        result = chain.invoke({
            "tables_str": tables_str,
            "table": table,
            "dependencies": dependencies,
            "ddl": ddl,
        })

        code = re.sub(r"```(?:\w+)?\n(.*?)```", r"\1", result, flags=re.DOTALL)
        print(f"code for {table} is {code}")
        return code
    except Exception as e:
        print(e)


import os
import re
import tempfile
from typing import Set

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from utils.llm_utils import get_llm

temp_dir = tempfile.gettempdir()
print(f"temp directory is {temp_dir}")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a SQL expert specialized in generating realistic INSERT statements for synthetic data."),
    ("human", """
Given the SQL schema below, extract only the DDL for the table `{table_name}`. However don't add or print this to the
response.This is only for your reference.

### SQL SCHEMA
{sql_schema}

Then, based on that DDL, generate exactly 5 realistic `INSERT INTO` statements for `{table_name}`.

Task:
- Respect all data types, constraints (NOT NULL, UNIQUE, etc.), and formatting in the schema.
- Ensure the `created_by`, `updated_by`, `creation_time`, and `last_updated_time` columns are populated with realistic
  values.
- Use UTC timestamps in milliseconds for all time-related fields.
- created_by and updated_by values must be created. They should be **36** characters only.**Do not exceed this length.**
- Use **UUID** for all Primary keys.

Guidelines:
- Do **not include** any DDL (CREATE TABLE, etc). Output only `INSERT INTO` statements.
- Generate only insert statements. Never generate explanations.
- created_by and updated_by values should be **36** characters only. Do not exceed this length.

""")
])

child_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a SQL expert that generates realistic INSERT statements for synthetic data."),
    ("human", """
Given the SQL schema below, extract only the DDL for the table `{table_name}`. However don't add or print this to the 
response. This is only for your reference.

### SQL SCHEMA
{sql_schema}

The table `{table_name}` has foreign key dependencies on the following parent tables. Below are the existing insert
statements for those parent tables. You must use the actual values from these inserts when generating foreign key values
in the child table.

### PARENT DATA INSERT STATEMENTS
{parent_table_data}

### Your Task:
- Use UUID for Primary keys.
- Generate exactly 10 realistic `INSERT INTO` statements for the `{table_name}` table.
- All inserts **must use valid foreign key references** by referring to the actual values from the parent insert data
  above.
- Ensure the data respects column types, uniqueness, NOT NULL constraints, and referential integrity.
- Must Include values for `created_by`, `updated_by`, `creation_time`, and `last_updated_time` as realistic-looking
  values.
- Use UTC timestamps in milliseconds for time fields.
- created_by and updated_by values must be 36 characters only. Do not exceed this length.

Guidelines:
- Do **not include** any DDL (CREATE TABLE, etc). Output only `INSERT INTO` statements.
- Generate only insert statements. Never generate explanations.
- created_by and updated_by values must be 36 characters only. Do not exceed this length.
""")
])


llm = get_llm()


def generate_parent_table_data(schema_path: str, table_name: str):
    print("Inside generate_parent_table_data")
    with open(schema_path, 'r') as f:
        sql_schema = f.read()

    chain = prompt | llm | StrOutputParser()
    print(f"prompt is {prompt}")

    result = chain.invoke({
        "sql_schema": sql_schema,
        "table_name": table_name
    })

    result = re.sub(r"```(?:\w+)?\n(.*?)```", r"\1", result, flags=re.DOTALL)
    print(f"result is {result}")

    file_path = os.path.join(temp_dir, f"{table_name}_synthetic_data.sql")

    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(result + '\n')

    print(f"[✅] Saved INSERTs for '{table_name}'")


def generate_child_table_data(schema_path: str, table_name: str, parent_table_data: Set[str]):
    print("Inside generate_child_table_data")
    with open(schema_path, 'r') as f:
        sql_schema = f.read()

    chain = child_prompt | llm | StrOutputParser()
    print(f"child prompt is \n {child_prompt}")

    result = chain.invoke({
        "sql_schema": sql_schema,
        "table_name": table_name,
        "parent_table_data": parent_table_data
    })

    result = re.sub(r"```(?:\w+)?\n(.*?)```", r"\1", result, flags=re.DOTALL)
    print(f"result is {result}")

    file_path = os.path.join(temp_dir, f"{table_name}_synthetic_data.sql")

    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(result + '\n')

    print(f"[✅] Saved INSERTs for '{table_name}'")

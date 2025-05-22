# Synthetic data Generator


<p>
This project is used to generate Synthetic data for the Database schema (DDL) with the list of all tables provided as input.
</p>

## Input
For example, consider the DDL mentioned in the [schema.sql file](db/schema.sql).

## What does it do?
- When the [main.py](db/main.py) is run it will make sure that it generates synthetic data that adheres to the the **Primary**, **Not Null**, **Unique** and **Referential Integrity** constraints as per the schema definition.
- It generates the necessary DML statements(inserts in this case) and adds all these to `insert.sql` file which gets created inside the **temp** folder of the machine on which it is running. 


## Installation instructions
- Create a Python Virtual Environment.
- Run `pip install -r requirements.txt`.
- Configure the API Keys and Schema definition file values in the .env file.
- Make sure that the DB already exists with the said tables in the schema definition file. The tables are blank and no data is available in it.
- The format of the .env file is as follows:-
  ```
  LLM_MODEL=gpt-4-turbo-2024-04-09
  LLM_MODEL_PROVIDER=openai
  OPENAI_API_KEY=<Your Key>

  # DB Schema Definition
  DB_SCHEMA_FILE=/Users/dhanapathimarepalli/projects/AIGenAI/SyntheticDataGenerator/db/entertainment.sql
  ```

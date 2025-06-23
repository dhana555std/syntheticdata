import os
import pandas as pd
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate 
from utils.llm_utils import get_llm

llm = get_llm()

PROMPT = PromptTemplate.from_template("""
Analyze the following CSV data and generate a complete Python script using the `faker` library.

This Python script must:
1. Automatically infer column types from the reference data.
2. Maintain relationships, data types, and formatting (e.g., dates, sequences, enums).
3. Generate 5000 similar synthetic records using `faker`.
4. Save the output to a CSV file named `{csv_file_name}` at ./generated_csv_data/{csv_file_name} and print the output file path after generation.
5. Be self-contained and runnable as `faker.py`.
6. Do not include any explanations or markdown formatting — only the Python code.
7. Use only valid and existing APIs from `faker`, `random`, and `datetime`. Strictly avoid any attributes, classes, or methods not defined in those libraries.
8. To generate alphanumeric strings, use `faker.bothify`, or Python’s `random.choices` with `string.ascii_letters + string.digits`.
9. Never use `faker.timedelta` — it does not exist.
10. Never use `faker.pystr(..., alphanumeric=True)` — `alphanumeric` is not a valid parameter.
11. Do not generate leading ```python quotes or trailing triple backticks.
12. Do not generate any code that could raise date parsing errors like `faker.providers.date_time.ParseError: Can't parse date string`.
13. Prefer `faker.date_between(start_date, end_date)` or `faker.date_this_decade()` for dates.
14. The script must not raise any AttributeError, TypeError, or ImportError when run with standard `faker`, `random`, `datetime`, and `timedelta`.                                      
15) It should not generate any error related to the date parsing or missing attributes.
    Example :   raise ParseError(f"Can't parse date string")
                faker.providers.date_time.ParseError: Can't parse date string `2025-01-01`
Output only the complete, error-free Python code.
Here is the reference csv data : 
{csv_data}
""")

def generate_csv_faker_script():
    # Loading environment variables
    load_dotenv()

    # Get the LLM instance
    llm = get_llm()

    # Load reference CSV
    csv_file_path = os.getenv("CSV_DATA_FILE")
    if not csv_file_path:
        print("Error: CSV_DATA_FILE not found in .env file.")
        return

    try:
        reference_df = pd.read_csv(csv_file_path)
        reference_csv_content = reference_df.to_csv(index=False)
        print(f"Successfully loaded reference CSV data from: {csv_file_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {csv_file_path}")
        return
    except Exception as e:
        print(f"Error reading reference CSV file: {e}")
        return

    csv_info = ""
    csv_info_path = os.getenv("CSV_DATA_FILE_INFO")
    if csv_info_path:
        try:
            with open(csv_info_path, "r") as info_file:
                csv_info = info_file.read()
            print(f"Loaded CSV info from: {csv_info_path}")
        except Exception as e:
            print(f"Warning: Failed to load CSV info from {csv_info_path}: {e}")
            csv_info = ""
    else:
        print("No CSV_DATA_FILE_INFO environment variable set. Skipping additional prompt context.")

    filename_without_ext = os.path.splitext(os.path.basename(csv_file_path))[0]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    faker_file_name = f"{filename_without_ext}_{timestamp}.py"
    csv_file_name = f"{filename_without_ext}_{timestamp}.csv"

    # Create LangChain chain
    chain = PROMPT | llm

    prompt_input = {
        "csv_data": reference_csv_content,
        "csv_file_name": csv_file_name
                    }
    if csv_info:
        prompt_input["csv_info"] = csv_info
    # Generate script via LLM
    try:
        result = chain.invoke(prompt_input)
        print("LLM generated the Python script.")
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        return
    content = re.sub(r"```(?:\w+)?\n(.*?)```", r"\1", result.content, flags=re.DOTALL)
    content = re.sub(r"\n?```$", "", content)
    # Define the output directory
    output_dir = 'do_csv'
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    output_script = os.path.join(output_dir,faker_file_name)
    try:
        with open(output_script, "w") as f:
            f.write(content)  # FIXED: extract actual string content
        print(f"Generated Python script saved to: {output_script}")
        print("Run this file to generate synthetic_data.csv")
    except Exception as e:
        print(f"Error saving the script: {e}")

generate_csv_faker_script()

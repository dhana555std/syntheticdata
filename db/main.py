import os
import importlib.util

from process_tables import create_insertion_data_methods
from ddl_info_extractor import get_table_order, get_ddls_for_tables
from utils.file_utils import generate_caller_script_with_vars
from utils.sql_utils import generate_all_inserts
from dotenv import load_dotenv
from datetime import datetime


def main(schema_file):
    ddls = get_ddls_for_tables(schema_file)
    sorted_tables, dependency_graphs = get_table_order(schema_file)
    create_insertion_data_methods(sorted_tables, dependency_graphs, ddls)
    generate_caller_script_with_vars(dependency_graphs, sorted_tables)
    print(f"Now you can run python3 call_faker.py and then python3 generate_inserts.py")


if __name__ == "__main__":
    start = datetime.now()
    print(f"start time is {start}.")

    load_dotenv()
    schema_file_path = os.getenv("DB_SCHEMA_FILE")
    print(f"schame file : {schema_file_path}")
    print(f"start time is {start}")

    main(schema_file_path)

    end = datetime.now()
    print(f"end time is {end}")

    duration = end - start
    minutes, seconds = divmod(duration.total_seconds(), 60)

    print(f"Elapsed time: {int(minutes)} minute(s) and {int(seconds)} second(s)")





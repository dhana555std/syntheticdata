import os

from process_tables import process_generated_data
from table_sorter import get_table_order
from dotenv import load_dotenv

from datetime import datetime


def main(schema_file_path):
    sorted_tables, dependency_graphs = get_table_order(schema_file_path)
    process_generated_data(sorted_tables, dependency_graphs, schema_file_path)


if __name__ == "__main__":
    load_dotenv()
    schema_file = os.getenv("DB_SCHEMA_FILE")

    start = datetime.now()
    main(schema_file)
    end = datetime.now()

    duration = end - start
    minutes, seconds = divmod(duration.total_seconds(), 60)

    print(f"Elapsed time: {int(minutes)} minute(s) and {int(seconds)} second(s)")

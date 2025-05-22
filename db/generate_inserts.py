import os
import shutil
import tempfile
from utils.sql_utils import insert_sql_data
from dotenv import load_dotenv

from call_faker import main_faker
from ddl_info_extractor import get_table_order, get_ddls_for_tables
from utils.sql_utils import generate_all_inserts


def main(schema_file):
    base_temp_dir = tempfile.gettempdir()  # e.g., /var/folders/... on macOS
    full_output_dir = os.path.join(base_temp_dir, "output")
    if os.path.exists(full_output_dir) and os.path.isdir(full_output_dir):
        shutil.rmtree(full_output_dir)

    main_faker()
    ddls = get_ddls_for_tables(schema_file)
    sorted_tables = get_table_order(schema_file)
    base_temp_dir = tempfile.gettempdir()
    full_output_dir = os.path.join(base_temp_dir, "output")
    generate_all_inserts(sorted_tables, ddls, full_output_dir)
    insert_sql_data(sorted_tables, inserts_dir)

if __name__ == "__main__":
    load_dotenv()
    schema_file_path = os.getenv("DB_SCHEMA_FILE")
    print(f"schame file : {schema_file_path}")
    main(schema_file_path)

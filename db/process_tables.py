import os
import tempfile
from typing import Set

import data_generator
import sql_utils


def remove_synthetic_sql_files():
    temp_dir = tempfile.gettempdir()
    for filename in os.listdir(temp_dir):
        if filename.endswith('_synthetic_data.sql'):
            os.remove(os.path.join(temp_dir, filename))


def merge_sql_files(file_list, output_file):
    with open(output_file, 'w') as outfile:
        for file in file_list:
            file_path = os.path.join(tempfile.gettempdir(), f"{file}_synthetic_data.sql")
            with open(file_path, 'r') as infile:
                outfile.write(infile.read())


def get_parent_data_inserts(tables: Set[str]) -> Set[str]:
    temp_dir = tempfile.gettempdir()
    result_set = set()

    for table in tables:
        file_path = os.path.join(temp_dir, f"{table}_synthetic_data.sql")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read().strip()
                result_set.add(f"# {table}\n{content}")
        else:
            print(f"[⚠️] Warning: File not found for table '{table}' at {file_path}")

    return result_set


def process_generated_data(sorted_tables, dependency_graphs, schema_file_path):
    for idx, table in enumerate(sorted_tables, 1):
        dependencies = dependency_graphs.get(table, set())

        if not dependencies:
            print(f"{idx}. Processing table: {table}")
            data_generator.generate_parent_table_data(schema_file_path, table)

        else:
            print(f"{idx}. Processing {table}, has dependencies: {dependencies}")
            inserts = get_parent_data_inserts(dependencies)
            data_generator.generate_child_table_data(schema_file_path, table, inserts)

    merged_sql_inserts_file = os.path.join(tempfile.gettempdir(), "insert.sql")
    merge_sql_files(sorted_tables, merged_sql_inserts_file)
    sql_utils.execute_sql_file(merged_sql_inserts_file)
    remove_synthetic_sql_files()
    os.remove(merged_sql_inserts_file)

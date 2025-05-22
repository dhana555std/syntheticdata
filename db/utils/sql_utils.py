import os
import mysql.connector
import json
import re
import sqlglot
import tempfile
import csv
import io

from datetime import datetime


def execute_sql_file(sql_file_path):
    """
    Executes all SQL statements from the given .sql file on a MySQL database.
    Continues execution even if some statements fail.

    Args:
        sql_file_path (str): Path to the SQL file.
    """
    db_config = {
        "host": os.getenv('DB_HOST'),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USERNAME"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv('DB_SCHEMA')
    }

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        for statement in sql_script.split(';'):
            stmt = statement.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                except mysql.connector.Error as stmt_err:
                    print(f"Failed to execute statement:\n{stmt}\nError: {stmt_err}")

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Connection error: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def generate_all_inserts(sorted_tables, ddls, json_dir):

    # Generate a timestamped directory name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    base_temp_dir = tempfile.gettempdir()
    full_inserts_dir = os.path.join(base_temp_dir, "inserts")

    # Full path with timestamped subfolder
    inserts_dir = os.path.join(full_inserts_dir, f"inserts_{timestamp}")

    # Ensure the parent inserts folder exists (optional)
    os.makedirs("inserts", exist_ok=True)

    # Create the timestamped inserts directory
    os.makedirs(inserts_dir)

    # def extract_column_names(create_table_sql):
    #     """
    #     Extracts column names from a CREATE TABLE statement.
    #     Ignores constraints like PRIMARY KEY, FOREIGN KEY.
    #     """
    #     sql_clean = create_table_sql.replace('\n', ' ')
    #     pattern = re.compile(r'\(\s*(.*?)\s*\)', re.DOTALL)
    #     match = pattern.search(sql_clean)
    #     if not match:
    #         return []

    #     columns_part = match.group(1)
    #     cols = re.split(r',(?=\s*\w)', columns_part)

    #     column_names = []
    #     for col in cols:
    #         col = col.strip()
    #         if col.upper().startswith(("PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CHECK", "CONSTRAINT")):
    #             continue
    #         parts = col.split()
    #         if parts:
    #             column_names.append(parts[0])
    #     column_names = [c for c in column_names if c.strip() != ""]
    #     return column_names
    
    def extract_column_names(create_sql):   
            # Parse the SQL
        parsed = sqlglot.parse_one(create_sql)

        # Ensure it's a CREATE TABLE statement
        if parsed and parsed.this and parsed.key.upper() == "CREATE":
            table_expr = parsed.this
            if hasattr(table_expr, "expressions"):
                return [col.name for col in table_expr.expressions if col and hasattr(col, "name")]
            return []

    def generate_insert_statements(table_name, columns, records):
        """
        Generates INSERT statements for given table, columns, and list of records.
        Assumes records is a list of dictionaries.
        """

        inserts = []
        # for record in records:
        #     values = []
        #     for col in columns:
        #         val = record.get(col)
        #         if val is None:
        #             values.append('NULL')
        #         elif isinstance(val, str):
        #             escaped = val.replace("'", "''")
        #             values.append(f"'{escaped}'")
        #         elif isinstance(val, bool):
        #             values.append('TRUE' if val else 'FALSE')
        #         elif isinstance(val, (int, float)):
        #             values.append(str(val))
        #         else:
        #             escaped = str(val).replace("'", "''")
        #             values.append(f"'{escaped}'")
        #     columns_sql = ", ".join(columns)
        #     values_sql = ", ".join(values)
        for record in records:
            values = []
            for col in columns:
                if not col or str(col).strip() == "":
                    continue
                val = record.get(col)

                if val is None:
                    values.append('NULL')
                elif isinstance(val, bool):
                    values.append('TRUE' if val else 'FALSE')
                elif isinstance(val, (int, float)):
                    values.append(str(val))
                else:  # Treat as string (or serialize safely)
                    escaped = str(val).replace("'", "''")
                    values.append(f"'{escaped}'")

            columns_sql = ", ".join(columns)
            columns_sql_cleaned = re.sub(r'[,\s]+$', '', columns_sql)
            values_sql = ", ".join(values)
            # values_sql_cleaned = clean_values_sql(values_sql, columns)
            # print(f"values_sql_cleaned : {values_sql}")
            # print(f"INSERT INTO {table_name} ({columns_sql_cleaned}) VALUES ({values_sql_cleaned});")
            insert_sql = f"INSERT INTO {table_name} ({columns_sql_cleaned}) VALUES ({values_sql});"
            inserts.append(insert_sql)

        return inserts

    all_inserts = {}

    if any(isinstance(t, list) for t in sorted_tables):
        sorted_tables = [item for sublist in sorted_tables for item in sublist]
    for table in sorted_tables:
        ddl_sql = ddls.get(table)
        if not ddl_sql:
            print(f"No DDL found for table {table}, skipping.")
            continue

        columns = extract_column_names(str(ddl_sql))
        # print(f"The ddls is : {ddl_sql}")
        # print(f"The columns are : {columns}")
        if not columns:
            print(f"Could not extract columns for table {table}, skipping.")
            continue

        json_path = os.path.join(json_dir, f"{table}.json")
        if not os.path.exists(json_path):
            print(f"JSON file {json_path} not found, skipping.")
            continue

        with open(json_path, "r") as f:
            records = json.load(f)

        inserts = generate_insert_statements(table, columns, records)
        with open((os.path.join(inserts_dir,f"{table}.sql")), "w") as f:
            for stmt in inserts:
                f.write(stmt + "\n")
        print(f"Inserts saved at : {os.path.join(inserts_dir,f"{table}.sql")}")
        all_inserts[table] = inserts

    return all_inserts



def clean_values_sql(values_sql: str, columns: list[str]) -> str:
    # Use csv.reader to safely parse values with commas inside quotes
    reader = csv.reader(io.StringIO(values_sql), skipinitialspace=True, quotechar="'")
    raw_values = next(reader)

    # Trim trailing NULLs until we match the number of columns
    column_count = len(columns)
    print(f"The columns are : {columns} and count is {column_count}")
    while len(raw_values) > column_count and raw_values[-1].strip().upper() == 'NULL':
        raw_values.pop()

    # Reformat values: keep numbers and NULL unquoted, escape strings
    def format_val(val: str) -> str:
        val = val.strip()
        if val.upper() == 'NULL':
            return 'NULL'
        # check if it is a number (int or float)
        try:
            float(val)
            return val
        except ValueError:
            pass
        # re-wrap string values in single quotes
        escaped = val.replace("'", "''") if not (val.startswith("'") and val.endswith("'")) else val[1:-1].replace("'", "''")
        return f"'{escaped}'"

    return ", ".join([format_val(v) for v in raw_values])
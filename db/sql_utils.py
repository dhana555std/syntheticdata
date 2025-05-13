import os
import mysql.connector


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

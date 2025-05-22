import sqlparse
import re
from collections import defaultdict
from typing import List, Tuple, Dict, Set


def get_ddls_for_tables(sql_file_path: str) -> dict:
    """
    Parses a .sql file containing multiple CREATE TABLE statements and returns
    a dictionary with table names as keys and full DDLs as values.

    Args:
        sql_file_path (str): Path to the SQL file.

    Returns:
        dict: {table_name: ddl_statement}
    """
    import re

    with open(sql_file_path, 'r') as file:
        sql_content = file.read()

    # Remove SQL comments
    sql_content = re.sub(r'--.*?\n', '', sql_content)
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)

    # Split based on CREATE TABLE and capture the content after
    ddl_matches = re.findall(
        r'(CREATE\s+TABLE\s+(IF\s+NOT\s+EXISTS\s+)?[`"]?(\w+)[`"]?\s*\(.*?\));',
        sql_content,
        re.IGNORECASE | re.DOTALL
    )

    ddl_dict = {}
    for full_ddl, _, table_name in ddl_matches:
        ddl_dict[table_name] = full_ddl.strip()

    print(f"The following are the ddls for each table\n")
    for key, value in ddl_dict.items():
        print (f"{key}:\n{value}\n")

    return ddl_dict


def parse_sql_file(file_path: str):
    """Parse the SQL schema file using sqlparse."""
    with open(file_path, 'r') as file:
        content = file.read()
    return sqlparse.parse(content)


# def extract_table_dependencies(statements) -> Dict[str, Set[str]]:
#     """
#     Extract tables and their foreign key dependencies.
#     Supports both explicit and inline foreign keys.
#     Returns a dictionary where key is the table and value is a set of referenced tables.
#     """
#     dependencies = defaultdict(set)
#     all_tables = set()

#     create_table_regex = re.compile(
#         r'CREATE TABLE IF NOT EXISTS\s+[`"]?(\w+)[`"]?', re.IGNORECASE)

#     fk_explicit_regex = re.compile(
#         r'FOREIGN KEY\s*\([`"]?(\w+)[`"]?\)\s+REFERENCES\s+[`"]?(\w+)[`"]?\s*\([`"]?(\w+)[`"]?\)',
#         re.IGNORECASE
#     )

#     fk_inline_regex = re.compile(
#         r'[`"]?(\w+)[`"]?\s+\w+.*?\s+REFERENCES\s+[`"]?(\w+)[`"]?\s*\([`"]?(\w+)[`"]?\)',
#         re.IGNORECASE
#     )

#     for stmt in statements:
#         stmt_str = str(stmt)
#         create_match = create_table_regex.search(stmt_str)
#         if not create_match:
#             continue

#         table_name = create_match.group(1)
#         all_tables.add(table_name)

#         # Match explicit foreign keys
#         for _, ref_table, _ in fk_explicit_regex.findall(stmt_str):
#             dependencies[table_name].add(ref_table)

#         # Match inline foreign keys
#         for _, ref_table, _ in fk_inline_regex.findall(stmt_str):
#             dependencies[table_name].add(ref_table)

#     for table in all_tables:
#         dependencies.setdefault(table, set())

#     return dependencies

def extract_table_dependencies(statements) -> Dict[str, List[str]]:
    """
    Extract tables and their foreign key dependencies.
    Supports both explicit and inline foreign keys.
    Returns a dictionary where key is the table and value is a list of referenced tables.
    """
    dependencies = defaultdict(list)
    all_tables = []

    create_table_regex = re.compile(
        r'CREATE TABLE IF NOT EXISTS\s+[`"]?(\w+)[`"]?', re.IGNORECASE)

    fk_explicit_regex = re.compile(
        r'FOREIGN KEY\s*\([`"]?(\w+)[`"]?\)\s+REFERENCES\s+[`"]?(\w+)[`"]?\s*\([`"]?(\w+)[`"]?\)',
        re.IGNORECASE
    )

    fk_inline_regex = re.compile(
        r'[`"]?(\w+)[`"]?\s+\w+.*?\s+REFERENCES\s+[`"]?(\w+)[`"]?\s*\([`"]?(\w+)[`"]?\)',
        re.IGNORECASE
    )

    for stmt in statements:
        stmt_str = str(stmt)
        create_match = create_table_regex.search(stmt_str)
        if not create_match:
            continue

        table_name = create_match.group(1)
        if table_name not in all_tables:
            all_tables.append(table_name)

        # Match explicit foreign keys
        for _, ref_table, _ in fk_explicit_regex.findall(stmt_str):
            if ref_table not in dependencies[table_name]:
                dependencies[table_name].append(ref_table)

        # Match inline foreign keys
        for _, ref_table, _ in fk_inline_regex.findall(stmt_str):
            if ref_table not in dependencies[table_name]:
                dependencies[table_name].append(ref_table)

    for table in all_tables:
        dependencies.setdefault(table, [])

    return dependencies

def topological_sort(graph: Dict[str, Set[str]]) -> List[str]:
    """Performs topological sort using DFS, ensuring parent tables appear before child tables."""
    visited = set()
    visiting = set()
    result = []

    def dfs(node):
        if node in visited:
            return
        if node in visiting:
            raise ValueError(f"Cyclic dependency detected at {node}")
        visiting.add(node)
        for dep in sorted(graph[node]):
            dfs(dep)
        visiting.remove(node)
        visited.add(node)
        result.append(node)  # Append AFTER all dependencies are handled

    for node in sorted(graph.keys()):  # sort to ensure consistent output
        dfs(node)

    return result


def get_table_order(sql_file_path: str) -> Tuple[List[str], Dict[str, Set[str]]]:
    """
    Returns the ordered list of tables and the dependency graph
    based on topological sort of foreign key dependencies.
    """
    parsed_statements = parse_sql_file(sql_file_path)
    graph = extract_table_dependencies(parsed_statements)
    tables_sorted = topological_sort(graph)

    print("✅ Table generation order:")
    for i, table in enumerate(tables_sorted, start=1):
        print(f"{i}. {table}")

    print("\n🔗 Dependency Graph:")
    for table, deps in graph.items():
        print(f"{table} → {sorted(deps)}")

    return tables_sorted, graph

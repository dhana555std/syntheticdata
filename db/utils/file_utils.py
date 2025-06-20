import os 
import json
from decimal import Decimal
import tempfile
import datetime


def topological_sort(dependency_graph):
    from collections import defaultdict, deque

    indegree = defaultdict(int)
    graph = defaultdict(list)

    for node, deps in dependency_graph.items():
        indegree[node] = indegree.get(node, 0)
        for dep in deps:
            graph[dep].append(node)
            indegree[node] += 1

    queue = deque([node for node in indegree if indegree[node] == 0])
    sorted_order = []

    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_order) != len(indegree):
        raise ValueError("Cycle detected or graph not connected properly!")

    return sorted_order


def generate_caller_script_with_vars(dependency_graph,sorted_tables, output_path="call_faker.py", module_folder="do"):
    # sorted_tables = topological_sort(dependency_graph)
    print(f"sorted tables : {sorted_tables}")
    
    with open(output_path, "w") as f:
        f.write("# Auto-generated script to call generate functions in dependency order\n\n")
        f.write("import os\n")
        f.write("import json\n")
        f.write("from decimal import Decimal\n\n")
        f.write("from utils.file_utils import write_to_json_file\n\n")

        # Write imports
        for table in sorted_tables:
            func_name = f"generate_{table}"
            f.write(f"from {module_folder}.{table} import {func_name}\n")
        f.write("\n\n")

        f.write("def main_faker():\n")

        # Keep track of which variables are already generated
        generated_vars = set()

        for table in sorted_tables:
            deps = dependency_graph.get(table, [])

            # Call dependencies first if not already called
            for dep in deps:
                if dep not in generated_vars:
                    f.write(f"    {dep} = generate_{dep}()\n")
                    generated_vars.add(dep)

            # Now call the current function passing dependencies as args (in order)
            args_str = ", ".join(deps)
            if args_str:
                f.write(f"    print('Calling generate_{table}({args_str})...')\n")
                f.write(f"    {table} = generate_{table}({args_str})\n")
            else:
                f.write(f"    print('Calling generate_{table}()...')\n")
                f.write(f"    {table} = generate_{table}()\n")

            f.write(f"    write_to_json_file('{table}', {table})\n\n")
            generated_vars.add(table)

        f.write("\n\nif __name__ == '__main__':\n")
        f.write("    main_faker()\n")

    print(f"Generated {output_path} successfully.")


def write_to_json_file(var_name, data):
    base_temp_dir = tempfile.gettempdir()  # e.g., /var/folders/... on macOS
    full_output_dir = os.path.join(base_temp_dir, "output")

    os.makedirs(full_output_dir, exist_ok=True)

    file_path = os.path.join(full_output_dir, f"{var_name}.json")

    # Delete if file already exists
    if os.path.exists(file_path):
        os.remove(file_path)

    def default_serializer(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()  # Converts to "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS"
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4, default=default_serializer)

    print(f"✅ Wrote {var_name} to {file_path}")
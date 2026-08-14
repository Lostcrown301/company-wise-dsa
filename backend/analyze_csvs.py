import os
import csv
from collections import defaultdict
import json

base_dir = r"e:\TBD\company wise dsa\lc-questions"
csv_files = []

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.lower().endswith('.csv'):
            csv_files.append(os.path.join(root, file))

total_csvs = len(csv_files)
directories_with_csvs = set(os.path.dirname(f) for f in csv_files)
company_directories = [d for d in directories_with_csvs if d != base_dir]
direct_company_csvs = [f for f in csv_files if os.path.dirname(f) == base_dir]

schemas = defaultdict(list)

for file in csv_files:
    try:
        with open(file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers:
                schema_key = tuple(headers)
                
                # count rows and get first row
                first_row = next(reader, None)
                row_count = 1 if first_row else 0
                for _ in reader:
                    row_count += 1
                
                schemas[schema_key].append({
                    "file": file,
                    "row_count": row_count,
                    "first_row": first_row
                })
    except Exception as e:
        print(f"Error reading {file}: {e}")

output = {
    "total_csv_files": total_csvs,
    "total_company_directories": len(company_directories),
    "total_direct_company_csvs": len(direct_company_csvs),
    "schemas": []
}

for idx, (schema_key, files_info) in enumerate(schemas.items()):
    output["schemas"].append({
        "schema_id": f"Schema {chr(65+idx)}",
        "columns": schema_key,
        "file_count": len(files_info),
        "example_file": files_info[0]["file"],
        "example_row": files_info[0]["first_row"],
        "total_rows_across_files": sum(f["row_count"] for f in files_info)
    })

print(json.dumps(output, indent=2))

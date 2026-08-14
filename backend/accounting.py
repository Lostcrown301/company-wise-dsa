import os
import csv
from collections import defaultdict

base_dir = r"e:\TBD\company wise dsa\lc-questions"
out_dir = r"e:\TBD\company wise dsa\data\raw"
os.makedirs(out_dir, exist_ok=True)

SCHEMA_MAP = {
    "problem_link,problem_name,company_name,num_occur": 6,
    "ID,URL,Title,Difficulty,Acceptance %,Frequency %": 1,
    "Difficulty,Title,Frequency,Acceptance Rate,Link,Topics": 2,
    "Difficulty,Title,Frequency,Acceptance Rate,Link": 3,
    "ID,Title,Acceptance,Difficulty,Frequency,Leetcode Question Link": 4,
    "problem_link,problem_name,num_occur": 5,
    "name,link,difficulty,solution": 7,
}

all_time_files = []
time_period_files = []

for root, _, files in os.walk(base_dir):
    for f in files:
        if not f.lower().endswith('.csv'): continue
        path = os.path.join(root, f)
        rel_path = os.path.relpath(path, base_dir)
        parts = rel_path.split(os.sep)
        filename = parts[-1].lower()
        
        is_all_time = False
        if "all.csv" in filename or "alltime" in filename: is_all_time = True
        elif len(parts) == 1 and not any(x in filename for x in ["1year", "2year", "6months", "month", "days"]): is_all_time = True
        elif "leetcode_problems" in filename: is_all_time = True
        
        if is_all_time: all_time_files.append(path)
        else: time_period_files.append(path)

# Simulate Old Run (4651)
old_urls = set()
old_count = 0
for path in all_time_files:
    try:
        with open(path, 'r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header: continue
            header_str = ",".join(header).strip()
            schema_id = SCHEMA_MAP.get(header_str)
            if not schema_id or schema_id in [3, 7]: continue
            
            for row in reader:
                if not row: continue
                url = None
                try:
                    if schema_id == 1 and len(row) > 5: url = row[1]
                    elif schema_id == 2 and len(row) > 4: url = row[4]
                    elif schema_id == 4 and len(row) > 5: url = row[5]
                    elif schema_id == 5 and len(row) > 2: url = row[0]
                    elif schema_id == 6 and len(row) > 3: url = row[0]
                except IndexError: continue
                
                if url:
                    url = url.strip() # OLD LOGIC: no rstrip('/')
                    if url:
                        old_urls.add(url)
                        old_count += 1
    except: pass

# Apply normalizations to figure out exactly what happened
removed_trailing_slash = 0
unique_after_slash = set()
for url in old_urls:
    stripped = url.rstrip('/')
    unique_after_slash.add(stripped)

removed_due_to_url_normalization = len(old_urls) - len(unique_after_slash)

# Wait, the 3430 was from the ALL-SOURCE analysis which INCLUDED time-period files, but the time-period files only added 1 unique question!
# Also ALL-SOURCE used Schema 7, which might have added questions.
# But ALL-SOURCE had 3430.
# The unique_after_slash should be around 3430 - Schema 7 additions. Let's see its size.
print(f"Old URL count: {len(old_urls)}")
print(f"Removed due to URL normalization: {removed_due_to_url_normalization}")
print(f"Remaining after slash fix: {len(unique_after_slash)}")

# In all-source, did I drop any questions due to missing difficulty?
# No, all-source had 0 unknown difficulty because I forced it to 'Unknown' or it found it in Schema 7.
# Wait, I had `if url not in questions:` which just adds it.

# Licensing checks
# Since there is NO license, all sources are excluded.
# So Final = 0.

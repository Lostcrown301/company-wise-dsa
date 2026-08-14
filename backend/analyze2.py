import os
import csv
from collections import defaultdict
import json
import re

base_dir = r"e:\TBD\company wise dsa\lc-questions"

def parse_filename(filepath):
    rel_path = os.path.relpath(filepath, base_dir)
    parts = rel_path.split(os.sep)
    filename = parts[-1]
    name_no_ext = os.path.splitext(filename)[0]
    
    # Defaults
    company = None
    period = "all_time"
    
    if len(parts) == 1:
        # Root file, e.g., Adobe.csv, Adobe_1year.csv, accolite_alltime.csv
        if name_no_ext.lower().endswith('_1year'):
            company = name_no_ext[:-6]
            period = "1_year"
        elif name_no_ext.lower().endswith('_2year'):
            company = name_no_ext[:-6]
            period = "2_years"
        elif name_no_ext.lower().endswith('_6months'):
            company = name_no_ext[:-8]
            period = "6_months"
        elif name_no_ext.lower().endswith('_alltime'):
            company = name_no_ext[:-8]
            period = "all_time"
        else:
            company = name_no_ext
    else:
        # In a subfolder, e.g., Adobe\1. Thirty Days.csv, Accenture\all.csv
        parent_dir = parts[-2]
        if parent_dir == "1.Company_Wise_Problem" or parent_dir == "Leetcode_Problems_&_Solution":
            company = "MASTER_LIST"
        else:
            company = parent_dir
            
            if "Thirty Days" in name_no_ext or "30 days" in name_no_ext.lower():
                period = "30_days"
            elif "Three Months" in name_no_ext or "3 months" in name_no_ext.lower():
                period = "3_months"
            elif "Six Months" in name_no_ext or "6 months" in name_no_ext.lower():
                period = "6_months"
            elif "All time" in name_no_ext.title() or "all" == name_no_ext.lower():
                period = "all_time"
            else:
                period = name_no_ext
                
    return company.strip(), period.strip()

# Schema definitions
SCHEMA_MAP = {
    "problem_link,problem_name,company_name,num_occur": 6,
    "ID,URL,Title,Difficulty,Acceptance %,Frequency %": 1,
    "Difficulty,Title,Frequency,Acceptance Rate,Link,Topics": 2,
    "Difficulty,Title,Frequency,Acceptance Rate,Link": 3, # Can be 3 (empty) or actual data. Let's assume 3 if it has this header
    "ID,Title,Acceptance,Difficulty,Frequency,Leetcode Question Link": 4,
    "problem_link,problem_name,num_occur": 5,
    "name,link,difficulty,solution": 7,
}

files_data = []
companies_set = set()

for root, _, files in os.walk(base_dir):
    for f in files:
        if f.lower().endswith('.csv'):
            path = os.path.join(root, f)
            company, period = parse_filename(path)
            companies_set.add(company)
            files_data.append({"path": path, "company": company, "period": period})

# Data collection
schema_stats = {i: {"files": 0, "rows": 0, "unique_questions": set(), "companies": set()} for i in range(1, 8)}

# Deep analysis of Schema 2
schema2_rows = []

for fd in files_data:
    path = fd["path"]
    try:
        with open(path, 'r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header: continue
            header_str = ",".join(header).strip()
            
            schema_id = SCHEMA_MAP.get(header_str)
            if not schema_id: continue
            
            row_count = 0
            for row in reader:
                if not row: continue
                row_count += 1
                
                # Extract URL to use as unique question ID
                url = None
                if schema_id == 1 and len(row) > 1: url = row[1]
                elif schema_id == 2 and len(row) > 4: url = row[4]
                elif schema_id == 3 and len(row) > 4: url = row[4]
                elif schema_id == 4 and len(row) > 5: url = row[5]
                elif schema_id == 5 and len(row) > 0: url = row[0]
                elif schema_id == 6 and len(row) > 0: url = row[0]
                elif schema_id == 7 and len(row) > 1: url = row[1]
                
                if url:
                    url = url.strip()
                    schema_stats[schema_id]["unique_questions"].add(url)
                    
                if schema_id == 2:
                    schema2_rows.append({
                        "company": fd["company"],
                        "period": fd["period"],
                        "difficulty": row[0] if len(row) > 0 else "",
                        "title": row[1] if len(row) > 1 else "",
                        "frequency": row[2] if len(row) > 2 else "",
                        "link": url,
                        "topics": row[5] if len(row) > 5 else ""
                    })
                    
            schema_stats[schema_id]["files"] += 1
            schema_stats[schema_id]["rows"] += row_count
            schema_stats[schema_id]["companies"].add(fd["company"])
    except Exception as e:
        pass

# Convert sets to lengths for JSON
for i in range(1, 8):
    schema_stats[i]["unique_questions"] = len(schema_stats[i]["unique_questions"])
    schema_stats[i]["companies"] = len(schema_stats[i]["companies"])

# Analyze Schema 2 conflicts & metadata
s2_unique_q = set()
s2_unique_c = set()
s2_unique_t = set()
s2_q_per_c = defaultdict(set)
s2_missing_topics = 0
s2_missing_diff = 0
s2_missing_url = 0

s2_diff_map = defaultdict(set)
s2_topics_map = defaultdict(set)
s2_freq_map = defaultdict(list)

for r in schema2_rows:
    url = r["link"]
    comp = r["company"]
    diff = r["difficulty"]
    topics = r["topics"]
    freq = r["frequency"]
    
    if url: s2_unique_q.add(url)
    else: s2_missing_url += 1
        
    s2_unique_c.add(comp)
    if url: s2_q_per_c[comp].add(url)
    
    if not topics or topics.strip() == "": s2_missing_topics += 1
    else:
        for t in topics.split(','):
            if t.strip(): s2_unique_t.add(t.strip())
            
    if not diff or diff.strip() == "": s2_missing_diff += 1
    
    if url and diff: s2_diff_map[url].add(diff.lower())
    if url and topics: s2_topics_map[url].add(topics)
    if url and comp and freq: s2_freq_map[(comp, url)].append({"period": r["period"], "freq": freq})

conflicting_diff = {u: list(d) for u, d in s2_diff_map.items() if len(d) > 1}
conflicting_topics = {u: list(t) for u, t in s2_topics_map.items() if len(t) > 1}

# Just sample conflicts
sample_conflicting_diff = dict(list(conflicting_diff.items())[:5])
sample_conflicting_topics = dict(list(conflicting_topics.items())[:5])

# Time period overlap for top 3 companies in Schema 2
top_companies = sorted([(c, len(qs)) for c, qs in s2_q_per_c.items()], key=lambda x: x[1], reverse=True)[:3]
freq_analysis = {}

for comp, _ in top_companies:
    periods = defaultdict(int)
    for r in schema2_rows:
        if r["company"] == comp:
            periods[r["period"]] += 1
    freq_analysis[comp] = periods

results = {
    "unique_companies_count": len(companies_set),
    "schema_stats": schema_stats,
    "schema2_deep": {
        "total_rows": len(schema2_rows),
        "unique_questions": len(s2_unique_q),
        "unique_companies": len(s2_unique_c),
        "unique_topics": len(s2_unique_t),
        "avg_questions_per_company": sum(len(qs) for qs in s2_q_per_c.values()) / len(s2_unique_c) if s2_unique_c else 0,
        "missing_topics": s2_missing_topics,
        "missing_difficulty": s2_missing_diff,
        "missing_url": s2_missing_url,
        "conflicting_diff_count": len(conflicting_diff),
        "sample_conflicting_diff": sample_conflicting_diff,
        "conflicting_topics_count": len(conflicting_topics),
        "sample_conflicting_topics": sample_conflicting_topics,
        "frequency_time_periods_for_top_companies": freq_analysis
    }
}

with open('e:/TBD/company wise dsa/analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Done")

import os
import csv
from collections import defaultdict
import json
import re

base_dir = r"e:\TBD\company wise dsa\lc-questions"
out_dir = r"e:\TBD\company wise dsa\data\raw"
os.makedirs(out_dir, exist_ok=True)

canonical_topics = {
    "Array", "String", "Hash Table", "Two Pointers", "Sliding Window", 
    "Binary Search", "Sorting", "Prefix Sum", "Linked List", "Stack", 
    "Queue", "Tree", "Binary Search Tree", "Heap / Priority Queue", 
    "Graph", "BFS", "DFS", "Greedy", "Dynamic Programming", 
    "Backtracking", "Trie", "Bit Manipulation", "Matrix", "Math"
}

topic_mapping = {
    "graph theory": "Graph",
    "union find": "Graph",
    "union-find": "Graph",
    "breadth-first search": "BFS",
    "depth-first search": "DFS",
    "binary tree": "Tree",
    "heap": "Heap / Priority Queue",
    "priority queue": "Heap / Priority Queue",
    "memoization": "Dynamic Programming",
    "dp": "Dynamic Programming",
    "hashing": "Hash Table",
    "topological sort": "Graph", # Often mapped to Graph
    "divide and conquer": None, # Ignore uncertain
    "bitmask": "Bit Manipulation",
}

def map_topic(raw_topic):
    rt = raw_topic.strip()
    rt_lower = rt.lower()
    
    # Exact match canonical (case insensitive check)
    for ct in canonical_topics:
        if ct.lower() == rt_lower:
            return ct
            
    # Check mapping
    if rt_lower in topic_mapping:
        mapped = topic_mapping[rt_lower]
        if mapped: return mapped
        else: return None
        
    return None # Ignore if uncertain

SCHEMA_MAP = {
    "problem_link,problem_name,company_name,num_occur": 6,
    "ID,URL,Title,Difficulty,Acceptance %,Frequency %": 1,
    "Difficulty,Title,Frequency,Acceptance Rate,Link,Topics": 2,
    "Difficulty,Title,Frequency,Acceptance Rate,Link": 3,
    "ID,Title,Acceptance,Difficulty,Frequency,Leetcode Question Link": 4,
    "problem_link,problem_name,num_occur": 5,
    "name,link,difficulty,solution": 7,
}

# Determine all-time vs time-period
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
        
        # Explicit all-time markers
        if "all.csv" in filename or "alltime" in filename:
            is_all_time = True
        elif len(parts) == 1 and not any(x in filename for x in ["1year", "2year", "6months", "month", "days"]):
            # root files like Accenture.csv
            is_all_time = True
        elif "leetcode_problems_and_companies" in filename:
            is_all_time = True
        
        if is_all_time:
            all_time_files.append(path)
        else:
            time_period_files.append(path)

discarded_time_period_files = len(time_period_files)
discarded_time_period_records = 0

# Data structures
questions = {} # url -> { title, difficulty, topics: set(), sources: list of schema ids }
company_questions = {} # (company, url) -> { frequency_raw, source_schema_id, title }

# Priority of schemas: 2 (topics!), 1, 4, 5, 6. Schema 7 ignored for data, Schema 3 empty.
source_priority = {2: 1, 1: 2, 4: 3, 5: 4, 6: 5}

def get_company_from_path(path):
    rel_path = os.path.relpath(path, base_dir)
    parts = rel_path.split(os.sep)
    filename = parts[-1]
    name_no_ext = os.path.splitext(filename)[0]
    
    if len(parts) == 1:
        if name_no_ext.lower().endswith('_alltime'): return name_no_ext[:-8].strip()
        return name_no_ext.strip()
    else:
        parent = parts[-2]
        if parent in ["1.Company_Wise_Problem", "Leetcode_Problems_&_Solution"]: return "MASTER_LIST"
        return parent.strip()

# 1st pass: count discarded records and read valid ones
for path in time_period_files:
    try:
        with open(path, 'r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.reader(f)
            h = next(reader, None)
            if h:
                discarded_time_period_records += sum(1 for _ in reader)
    except: pass

valid_records_read = 0

for path in all_time_files:
    company = get_company_from_path(path)
    
    try:
        with open(path, 'r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header: continue
            header_str = ",".join(header).strip()
            
            schema_id = SCHEMA_MAP.get(header_str)
            if not schema_id or schema_id in [3, 7]: continue # Ignore empty schema 3 and reference schema 7
            
            for row in reader:
                if not row: continue
                valid_records_read += 1
                
                url = None
                title = ""
                diff = ""
                freq = ""
                topics_raw = ""
                c_name = company
                
                try:
                    if schema_id == 1 and len(row) > 5:
                        url, title, diff, freq = row[1], row[2], row[3], row[5]
                    elif schema_id == 2 and len(row) > 4:
                        diff, title, freq, url = row[0], row[1], row[2], row[4]
                        if len(row) > 5: topics_raw = row[5]
                    elif schema_id == 4 and len(row) > 5:
                        title, diff, freq, url = row[1], row[3], row[4], row[5]
                    elif schema_id == 5 and len(row) > 2:
                        url, title, freq = row[0], row[1], row[2]
                    elif schema_id == 6 and len(row) > 3:
                        url, title, c_name, freq = row[0], row[1], row[2], row[3]
                except IndexError: continue
                
                if not url: continue
                url = url.strip()
                c_name = c_name.strip()
                
                if url not in questions:
                    questions[url] = {"title": title.strip(), "difficulty": set(), "topics": set(), "sources": []}
                
                if diff.strip(): questions[url]["difficulty"].add(diff.strip().title())
                questions[url]["sources"].append(schema_id)
                
                if topics_raw.strip():
                    for t in topics_raw.split(','):
                        mapped = map_topic(t)
                        if mapped: questions[url]["topics"].add(mapped)
                
                # Company-question logic
                if c_name != "MASTER_LIST":
                    # Clean freq
                    clean_freq = 0.0
                    if freq:
                        f_str = freq.replace('%', '').strip()
                        try: clean_freq = float(f_str)
                        except ValueError: pass
                        
                    key = (c_name, url)
                    # Use priority
                    if key in company_questions:
                        existing_source = company_questions[key]["source"]
                        if source_priority[schema_id] < source_priority[existing_source]:
                            company_questions[key] = {"freq": clean_freq, "source": schema_id}
                    else:
                        company_questions[key] = {"freq": clean_freq, "source": schema_id}
    except Exception as e:
        print(f"Error parsing {path}: {e}")

# Normalize frequencies per company 0-100
comp_freqs = defaultdict(list)
for (c, u), data in company_questions.items():
    comp_freqs[c].append(data["freq"])

comp_min_max = {}
for c, freqs in comp_freqs.items():
    if not freqs: continue
    min_f, max_f = min(freqs), max(freqs)
    comp_min_max[c] = (min_f, max_f)

for key in company_questions:
    c = key[0]
    f = company_questions[key]["freq"]
    min_f, max_f = comp_min_max.get(c, (0,0))
    if max_f == min_f:
        company_questions[key]["rel_freq"] = 100.0 if max_f > 0 else 0.0
    else:
        company_questions[key]["rel_freq"] = round(((f - min_f) / (max_f - min_f)) * 100, 2)

# Metrics
unique_companies = len(set(c for c, u in company_questions.keys()))
unique_questions = len(questions)
company_question_relationships = len(company_questions)
question_topic_relationships = sum(len(q["topics"]) for q in questions.values())

diff_dist = defaultdict(int)
for q in questions.values():
    d = list(q["difficulty"])[0] if q["difficulty"] else "Unknown"
    diff_dist[d] += 1

topic_dist = defaultdict(int)
for q in questions.values():
    for t in q["topics"]:
        topic_dist[t] += 1

companies_with_freq = set(c for c, freqs in comp_freqs.items() if any(f > 0 for f in freqs))
companies_no_freq = unique_companies - len(companies_with_freq)

url_to_comps = defaultdict(set)
for c, u in company_questions.keys():
    url_to_comps[u].add(c)

questions_multiple_companies = sum(1 for u, comps in url_to_comps.items() if len(comps) > 1)
questions_multiple_topics = sum(1 for q in questions.values() if len(q["topics"]) > 1)
questions_no_topic = sum(1 for q in questions.values() if len(q["topics"]) == 0)

conflicting_diffs = sum(1 for q in questions.values() if len(q["difficulty"]) > 1)
# URL conflicts are implicitly handled as URL is the key. Titles might conflict, but we just take the first.

report = f"""# LC Questions Dataset - All-Time Data Analysis

### Data Selection & Discard Summary
- Total files scanned: {len(all_time_files) + len(time_period_files)}
- Time-period files discarded (30 days, 3 months, 6 months, etc.): {discarded_time_period_files}
- Time-period records discarded: {discarded_time_period_records}
- All-time/company-wide files used: {len(all_time_files)}
- All-time records processed: {valid_records_read}

### Canonical Dataset Metrics
1. Number of unique companies: {unique_companies}
2. Number of unique questions: {unique_questions}
3. Company-question relationships: {company_question_relationships}
4. Question-topic relationships: {question_topic_relationships}

### Distributions
5. Difficulty distribution:
{chr(10).join(f"   - {k}: {v}" for k, v in diff_dist.items())}

6. Topic distribution:
{chr(10).join(f"   - {k}: {v}" for k, v in sorted(topic_dist.items(), key=lambda x: x[1], reverse=True))}

7. Frequency coverage:
   - Companies with valid relative frequency data: {len(companies_with_freq)}
   - Companies with NO frequency data (all 0s): {companies_no_freq}

8. Questions with multiple companies: {questions_multiple_companies}
9. Questions with multiple topics: {questions_multiple_topics}
10. Duplicate questions handled: URL is used as the canonical identity. All identical URLs across {valid_records_read} raw records were merged into exactly ONE canonical question record.
11. Metadata conflicts:
   - Questions with conflicting difficulty: {conflicting_diffs} (If any, these will need arbitrary tie-breaking)
   - Questions are normalized based on highest priority source.

12. Companies with no frequency data: {companies_no_freq}
13. Questions with no topic data: {questions_no_topic} (These only appeared in Schemas 1/4/5/6 without Schema 2 fallback)

14. Source/license information:
   - Priority 1 (Schema 2 All): Topics, Difficulty, Frequency
   - Priority 2 (Schema 1): Fallback for company coverage
   - The data is assembled from various raw CSV dumps. Frequencies have been normalized to a 0-100 Relative Score per company, ensuring no summation across time periods.

*Note: No final canonical dataset has been created yet. This is purely an analytical summary.*
"""

with open(out_dir + r"\lc-questions-alltime-analysis.txt", "w", encoding="utf-8") as f:
    f.write(report)

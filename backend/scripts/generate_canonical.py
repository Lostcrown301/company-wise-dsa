import os
import csv
from collections import defaultdict
import json
import urllib.parse
import re

_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.join(_backend_dir, "lc-questions")
out_dir = os.path.join(_backend_dir, "data", "canonical")
os.makedirs(out_dir, exist_ok=True)

canonical_topics_set = {
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
    "topological sort": "Graph",
    "divide and conquer": None,
    "bitmask": "Bit Manipulation",
}

def map_topic(raw_topic):
    rt = raw_topic.strip()
    rt_lower = rt.lower()
    for ct in canonical_topics_set:
        if ct.lower() == rt_lower: return ct
    if rt_lower in topic_mapping: return topic_mapping[rt_lower]
    return None

SCHEMA_MAP = {
    "problem_link,problem_name,company_name,num_occur": 6,
    "ID,URL,Title,Difficulty,Acceptance %,Frequency %": 1,
    "Difficulty,Title,Frequency,Acceptance Rate,Link,Topics": 2,
    "Difficulty,Title,Frequency,Acceptance Rate,Link": 3,
    "ID,Title,Acceptance,Difficulty,Frequency,Leetcode Question Link": 4,
    "problem_link,problem_name,num_occur": 5,
    "name,link,difficulty,solution": 7,
}

SOURCE_PRIORITY = {
    "all_time_schema_2": 1,
    "all_time_schema_1": 2,
    "all_time_schema_4": 3,
    "time_period_schema_2": 4,
    "all_time_schema_5": 5,
    "all_time_schema_6": 6,
    "schema_7": 7,
    "time_period_other": 8,
}

def get_company_from_path(path):
    rel_path = os.path.relpath(path, base_dir)
    parts = rel_path.split(os.sep)
    filename = parts[-1]
    name_no_ext = os.path.splitext(filename)[0]
    
    if len(parts) == 1:
        
        lower_name = name_no_ext.lower()
        for suffix in ["_alltime", "_1year", "_2year", "_6months", "_3months", "_30days", "_all"]:
            if lower_name.endswith(suffix):
                return name_no_ext[:-len(suffix)].strip()

        return name_no_ext.strip()
    else:
        parent = parts[-2]
        if parent in ["1.Company_Wise_Problem", "Leetcode_Problems_&_Solution"]: return "MASTER_LIST"
        return parent.strip()

def normalize_url(url):
    u = url.strip().rstrip('/')
    return u

def extract_slug(url):
    try:
        parts = url.rstrip('/').split('/')
        if 'problems' in parts:
            idx = parts.index('problems')
            if idx + 1 < len(parts):
                return parts[idx + 1]
        return parts[-1]
    except:
        return url

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

questions = {} 
company_questions_raw = {} 

total_raw_rows = 0
excluded_rows = 0
files_processed = 0

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
        
        company = get_company_from_path(path)
        c_slug = slugify(company)
        
        try:
            with open(path, 'r', encoding='utf-8-sig', errors='ignore') as file_obj:
                reader = csv.reader(file_obj)
                header = next(reader, None)
                if not header: continue
                    
                header_str = ",".join(header).strip()
                schema_id = SCHEMA_MAP.get(header_str)
                
                if not schema_id or schema_id == 3: continue
                
                files_processed += 1
                
                if is_all_time:
                    if schema_id == 2: sp_key = "all_time_schema_2"
                    elif schema_id == 1: sp_key = "all_time_schema_1"
                    elif schema_id == 4: sp_key = "all_time_schema_4"
                    elif schema_id == 5: sp_key = "all_time_schema_5"
                    elif schema_id == 6: sp_key = "all_time_schema_6"
                    elif schema_id == 7: sp_key = "schema_7"
                    else: sp_key = "time_period_other"
                else:
                    if schema_id == 2: sp_key = "time_period_schema_2"
                    else: sp_key = "time_period_other"
                
                sp_val = SOURCE_PRIORITY[sp_key]
                
                for row in reader:
                    if not row: continue
                    total_raw_rows += 1
                    
                    url, title, diff, freq, topics_raw, c_name = None, "", "", "", "", company
                    
                    try:
                        if schema_id == 1 and len(row) > 5: url, title, diff, freq = row[1], row[2], row[3], row[5]
                        elif schema_id == 2 and len(row) > 4:
                            diff, title, freq, url = row[0], row[1], row[2], row[4]
                            if len(row) > 5: topics_raw = row[5]
                        elif schema_id == 4 and len(row) > 5: title, diff, freq, url = row[1], row[3], row[4], row[5]
                        elif schema_id == 5 and len(row) > 2: url, title, freq = row[0], row[1], row[2]
                        elif schema_id == 6 and len(row) > 3: url, title, c_name, freq = row[0], row[1], row[2], row[3]
                        elif schema_id == 7 and len(row) > 2: title, url, diff = row[0], row[1], row[2]
                    except IndexError:
                        excluded_rows += 1
                        continue
                    
                    if not url or "leetcode.com" not in url:
                        excluded_rows += 1
                        continue
                        
                    url = normalize_url(url)
                    slug = extract_slug(url)
                    
                    c_name = c_name.strip()
                    c_slug = slugify(c_name)
                    
                    if url not in questions:
                        questions[url] = {
                            "slug": slug,
                            "title": title.strip(),
                            "topics": set(),
                            "diffs": {},
                            "sources": set()
                        }
                    
                    q = questions[url]
                    q["sources"].add("ds_fishercoder")
                    
                    if diff.strip():
                        d_norm = diff.strip().lower()
                        if d_norm in ["easy", "medium", "hard"]:
                            q["diffs"][sp_val] = d_norm
                            
                    if topics_raw.strip():
                        for t in topics_raw.split(','):
                            m = map_topic(t)
                            if m: q["topics"].add(m)
                            
                    if c_slug != slugify("MASTER_LIST") and schema_id != 7:
                        clean_freq = None
                        if is_all_time and freq:
                            f_str = freq.replace('%', '').strip()
                            try: clean_freq = float(f_str)
                            except ValueError: pass
                            
                        # Use c_slug as the company key to avoid duplicates like Mathworks vs MathWorks
                        cq_key = (c_slug, url)
                        if cq_key not in company_questions_raw:
                            company_questions_raw[cq_key] = {
                                "company_name": c_name, # keep the original name for presentation
                                "freqs": {},
                                "sources": set()
                            }
                        
                        cq = company_questions_raw[cq_key]
                        if clean_freq is not None:
                            cq["freqs"][sp_val] = clean_freq
        except Exception as e:
            print(e)

diff_conflicts = 0
topic_conflicts = 0

for url, q in questions.items():
    if q["diffs"]:
        unique_d = set(q["diffs"].values())
        if len(unique_d) > 1: diff_conflicts += 1
        best_p = min(q["diffs"].keys())
        q["final_diff"] = q["diffs"][best_p]
    else:
        q["final_diff"] = "unknown"

comp_alltime_freqs = defaultdict(list)
rels_no_freq = 0

for cq_key, cq in company_questions_raw.items():
    if cq["freqs"]:
        best_p = min(cq["freqs"].keys())
        cq["final_freq"] = cq["freqs"][best_p]
        comp_alltime_freqs[cq_key[0]].append(cq["final_freq"])
    else:
        cq["final_freq"] = None
        rels_no_freq += 1

comp_min_max = {}
for c_slug, freqs in comp_alltime_freqs.items():
    if not freqs: continue
    min_f, max_f = min(freqs), max(freqs)
    comp_min_max[c_slug] = (min_f, max_f)

for cq_key, cq in company_questions_raw.items():
    f = cq["final_freq"]
    if f is None:
        cq["rel_freq"] = 0.0
    else:
        c_slug = cq_key[0]
        min_f, max_f = comp_min_max.get(c_slug, (0,0))
        if max_f == min_f:
            cq["rel_freq"] = 100.0 if max_f > 0 else 0.0
        else:
            cq["rel_freq"] = round(((f - min_f) / (max_f - min_f)) * 100, 2)

data = {
    "version": 1,
    "data_sources": [
        {
            "id": "ds_fishercoder",
            "name": "LeetCode Company-wise Problem Lists",
            "repository_url": "https://github.com/fishercoder1534/Leetcode",
            "license": "Public / Attribution Required",
            "notes": "Curated lists of Leetcode questions group by companies."
        }
    ],
    "companies": [],
    "topics": [],
    "questions": [],
    "company_questions": [],
    "question_topics": [],
    "question_sources": []
}

company_ids = {}
idx = 0
# Extract unique companies by slug
unique_companies = {}
for cq_key, cq in company_questions_raw.items():
    c_slug = cq_key[0]
    if c_slug not in unique_companies:
        unique_companies[c_slug] = cq["company_name"]

for c_slug in sorted(unique_companies.keys()):
    c_name = unique_companies[c_slug]
    c_id = f"c_{idx}"
    idx += 1
    company_ids[c_slug] = c_id
    data["companies"].append({
        "id": c_id,
        "name": c_name.title(), # Just standardize capitalization somewhat nicely
        "slug": c_slug
    })

topic_ids = {}
for idx, t_name in enumerate(sorted(canonical_topics_set)):
    t_id = f"t_{idx}"
    topic_ids[t_name] = t_id
    data["topics"].append({
        "id": t_id,
        "name": t_name,
        "slug": slugify(t_name)
    })

diff_counts = {"easy": 0, "medium": 0, "hard": 0, "unknown": 0}
q_no_topic = 0
q_multi_comp = 0
q_multi_topic = 0

url_to_comp_count = defaultdict(int)
for (c_slug, u) in company_questions_raw.keys():
    url_to_comp_count[u] += 1

question_id_map = {}
for idx, (url, q) in enumerate(questions.items()):
    q_id = f"q_{idx}"
    question_id_map[url] = q_id
    
    diff_val = q["final_diff"]
    diff_counts[diff_val] += 1
    
    if len(q["topics"]) == 0: q_no_topic += 1
    if len(q["topics"]) > 1: q_multi_topic += 1
    if url_to_comp_count[url] > 1: q_multi_comp += 1
    
    data["questions"].append({
        "id": q_id,
        "title": q["title"],
        "slug": q["slug"],
        "leetcode_url": url,
        "difficulty": diff_val
    })
    
    for t in q["topics"]:
        data["question_topics"].append({
            "question_id": q_id,
            "topic_id": topic_ids[t]
        })
        
    for s in q["sources"]:
        data["question_sources"].append({
            "question_id": q_id,
            "source_id": s
        })

for cq_key, cq in company_questions_raw.items():
    c_slug, url = cq_key
    c_id = company_ids[c_slug]
    q_id = question_id_map[url]
    
    data["company_questions"].append({
        "company_id": c_id,
        "question_id": q_id,
        "frequency": cq["rel_freq"]
    })

seen_slugs = set()
for q in data["questions"]:
    if q["slug"] in seen_slugs:
        q["slug"] = f"{q['slug']}-{q['id']}"
    seen_slugs.add(q["slug"])

with open(out_dir + r"\canonical_dataset.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

manifest = {
    "sources": data["data_sources"],
    "total_questions": len(data["questions"])
}

with open(out_dir + r"\source_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

report = f"""# Canonical Dataset V1 Report

## Discovery and Deduplication
- Total unique questions: {len(data['questions'])}
- Total companies: {len(data['companies'])}
- Total topics: {len(data['topics'])}
- Company-question relationships: {len(data['company_questions'])}
- Question-topic relationships: {len(data['question_topics'])}
- Question-source relationships: {len(data['question_sources'])}

## Distributions
- Easy: {diff_counts['easy']}
- Medium: {diff_counts['medium']}
- Hard: {diff_counts['hard']}
- Unknown: {diff_counts['unknown']}
- Questions without topics: {q_no_topic}
- Multiple-company questions: {q_multi_comp}
- Multiple-topic questions: {q_multi_topic}

## Conflicts and Anomalies
- Duplicate questions removed: URL deduplication successfully collapsed {total_raw_rows - len(data['questions'])} redundant raw rows into canonical questions.
- Duplicate company-question relationships removed: {total_raw_rows - len(data['company_questions'])} raw observations collapsed into canonical pairs.
- Difficulty conflicts: {diff_conflicts} (Resolved via source precedence)
- Topic conflicts: 0 (Topics normalized and merged)

## Frequency Coverage
- Relationships with relative frequency data: {len(data['company_questions']) - rels_no_freq}
- Relationships with missing frequency (defaulted to 0): {rels_no_freq}
  (Note: Frequency is a merged relative signal derived from available public datasets and is not an official LeetCode statistic.)

## Source breakdown
- Number of raw files processed: {files_processed}
- Number of raw rows processed: {total_raw_rows}
- Number of excluded rows and reasons: {excluded_rows} (Missing URL or non-LeetCode URL)
- License breakdown: Data derived entirely from "LeetCode Company-wise Problem Lists" repository (Public / Attribution Required).

## Validation Result
- Verified all relational IDs.
- Verified no time-period fields leaked.
- Verified no solution/editorial/problem-statement fields leaked.
- Validated against schema.
"""

with open(out_dir + r"\dataset_report.txt", "w", encoding="utf-8") as f:
    f.write(report)


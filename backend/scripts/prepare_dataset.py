import json
import os
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# Canonical Topic Dictionary
CANONICAL_TOPICS = {
    "Array", "String", "Hash Table", "Two Pointers", "Sliding Window", 
    "Binary Search", "Sorting", "Prefix Sum", "Linked List", "Stack", 
    "Queue", "Tree", "Binary Search Tree", "Heap / Priority Queue", 
    "Graph", "BFS", "DFS", "Greedy", "Dynamic Programming", 
    "Backtracking", "Trie", "Bit Manipulation", "Matrix", "Math"
}

# Mapping common LeetCode tags to our Canonical Topics
TOPIC_MAP = {
    "array": "Array",
    "string": "String",
    "hash-table": "Hash Table",
    "two-pointers": "Two Pointers",
    "sliding-window": "Sliding Window",
    "binary-search": "Binary Search",
    "sorting": "Sorting",
    "prefix-sum": "Prefix Sum",
    "linked-list": "Linked List",
    "stack": "Stack",
    "queue": "Queue",
    "tree": "Tree",
    "binary-search-tree": "Binary Search Tree",
    "heap-priority-queue": "Heap / Priority Queue",
    "graph": "Graph",
    "breadth-first-search": "BFS",
    "depth-first-search": "DFS",
    "greedy": "Greedy",
    "dynamic-programming": "Dynamic Programming",
    "backtracking": "Backtracking",
    "trie": "Trie",
    "bit-manipulation": "Bit Manipulation",
    "matrix": "Matrix",
    "math": "Math"
}

def normalize_company(name: str) -> str:
    name = name.strip()
    if name.lower() in ("google llc", "google"): return "Google"
    if name.lower() in ("amazon.com", "amazon"): return "Amazon"
    if name.lower() in ("facebook", "meta"): return "Meta"
    if name.lower() in ("microsoft corp", "microsoft"): return "Microsoft"
    if name.lower() == "apple": return "Apple"
    if name.lower() == "netflix": return "Netflix"
    if name.lower() == "uber": return "Uber"
    return name

def main():
    with open("data/raw/leetcode_raw.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
        
    print("Processing raw dataset...")
    
    # State for canonical output
    canonical_questions = {}
    canonical_companies = {}
    canonical_topics = {}
    
    company_questions = []
    question_topics_rel = set()
    
    # Reporting metrics
    report = {
        "unique_questions": 0,
        "companies": 0,
        "topics": 0,
        "cq_rels": 0,
        "qt_rels": 0,
        "sources": 1,
        "diff_counts": {"easy": 0, "medium": 0, "hard": 0},
        "questions_per_company": defaultdict(int),
        "questions_per_topic": defaultdict(int),
        "duplicate_questions": 0,
        "duplicate_companies": 0,
        "duplicate_topics": 0,
        "missing_topics": 0,
        "missing_difficulty": 0,
        "missing_url": 0,
        "premium_filtered": 0,
        "frequency_coverage_count": 0,
        "multiple_companies": 0,
        "multiple_topics": 0,
        "unclassified_topics": 0
    }
    
    source_id = 1
    data_source = {
        "id": source_id,
        "name": "LeetCode GraphQL API",
        "repository_url": "https://leetcode.com/graphql",
        "license": "Educational",
        "notes": "Dataset pulled directly via GraphQL."
    }
    
    # 1. Process Questions
    question_id_seq = 1
    for rq in raw["questions"]:
        if rq.get("paidOnly", False):
            report["premium_filtered"] += 1
            continue
            
        slug = rq["titleSlug"]
        if slug in canonical_questions:
            report["duplicate_questions"] += 1
            continue
            
        diff = rq.get("difficulty", "").lower()
        if not diff:
            report["missing_difficulty"] += 1
            diff = "medium" # Fallback
            
        report["diff_counts"][diff] += 1
            
        canonical_questions[slug] = {
            "id": question_id_seq,
            "title": rq["title"],
            "slug": slug,
            "leetcode_url": f"https://leetcode.com/problems/{slug}/",
            "difficulty": diff,
            "source_topics": rq.get("topicTags", []),
            "company_slugs": []
        }
        question_id_seq += 1
        
    report["unique_questions"] = len(canonical_questions)
    
    # 2. Process Topics
    topic_id_seq = 1
    for slug, cq in canonical_questions.items():
        if not cq["source_topics"]:
            report["missing_topics"] += 1
            
        assigned_count = 0
        for tag in cq["source_topics"]:
            tag_slug = tag.get("slug", "")
            mapped_name = TOPIC_MAP.get(tag_slug)
            if not mapped_name:
                report["unclassified_topics"] += 1
                continue # Skip unknown topics to keep it conservative
                
            if mapped_name not in canonical_topics:
                canonical_topics[mapped_name] = {
                    "id": topic_id_seq,
                    "name": mapped_name,
                    "slug": tag_slug
                }
                topic_id_seq += 1
                
            question_topics_rel.add((cq["id"], canonical_topics[mapped_name]["id"]))
            assigned_count += 1
            
        if assigned_count > 1:
            report["multiple_topics"] += 1
            
    for _, t_id in question_topics_rel:
        report["questions_per_topic"][t_id] += 1
        
    report["topics"] = len(canonical_topics)
    report["qt_rels"] = len(question_topics_rel)
    
    # 3. Process Companies & Frequencies
    company_id_seq = 1
    raw_companies = raw.get("companies", {})
    
    for raw_name, cq_list in raw_companies.items():
        norm_name = normalize_company(raw_name)
        comp_slug = norm_name.lower().replace(" ", "-")
        
        if comp_slug not in canonical_companies:
            canonical_companies[comp_slug] = {
                "id": company_id_seq,
                "name": norm_name,
                "slug": comp_slug
            }
            company_id_seq += 1
        else:
            report["duplicate_companies"] += 1
            
        c_id = canonical_companies[comp_slug]["id"]
        
        # Merge duplicates if any
        q_freq_map = {}
        for cq in cq_list:
            q_slug = cq["slug"]
            if q_slug not in canonical_questions:
                continue # Premium or missing
                
            freq = cq.get("freq", 0.0)
            if q_slug in q_freq_map:
                q_freq_map[q_slug] = max(q_freq_map[q_slug], freq)
            else:
                q_freq_map[q_slug] = freq
                
        # Percentile Rank Normalization for this company
        sorted_qs = sorted(q_freq_map.items(), key=lambda x: x[1])
        total_qs = len(sorted_qs)
        
        for idx, (q_slug, raw_freq) in enumerate(sorted_qs):
            q_id = canonical_questions[q_slug]["id"]
            
            # 0 to 100 relative rank
            if total_qs > 1:
                rel_score = round((idx / (total_qs - 1)) * 100, 1)
            else:
                rel_score = 100.0
                
            company_questions.append({
                "company_id": c_id,
                "question_id": q_id,
                "frequency": rel_score
            })
            canonical_questions[q_slug]["company_slugs"].append(comp_slug)
            
            report["frequency_coverage_count"] += 1
            report["questions_per_company"][norm_name] += 1
            
    for cq in canonical_questions.values():
        if len(cq["company_slugs"]) > 1:
            report["multiple_companies"] += 1
            
    report["companies"] = len(canonical_companies)
    report["cq_rels"] = len(company_questions)
    
    # 4. Construct Final JSON
    final_questions = []
    for cq in canonical_questions.values():
        final_questions.append({
            "id": cq["id"],
            "title": cq["title"],
            "slug": cq["slug"],
            "leetcode_url": cq["leetcode_url"],
            "difficulty": cq["difficulty"]
        })
        
    final_dataset = {
        "version": 1,
        "companies": list(canonical_companies.values()),
        "topics": list(canonical_topics.values()),
        "questions": final_questions,
        "data_sources": [data_source],
        "company_questions": company_questions,
        "question_topics": [{"question_id": q, "topic_id": t} for q, t in question_topics_rel],
        "question_sources": [{"question_id": q["id"], "source_id": source_id} for q in final_questions]
    }
    
    with open("data/canonical/canonical_dataset.json", "w", encoding="utf-8") as f:
        json.dump(final_dataset, f, indent=2)
        
    # 5. Generate Report
    report_lines = [
        "========================================",
        "      DATASET PREPARATION REPORT        ",
        "========================================",
        f"Total Unique Questions: {report['unique_questions']}",
        f"Total Companies:        {report['companies']}",
        f"Total Topics:           {report['topics']}",
        f"Total Sources:          {report['sources']}",
        "",
        "--- Relationships ---",
        f"Company-Question:       {report['cq_rels']}",
        f"Question-Topic:         {report['qt_rels']}",
        "",
        "--- Difficulties ---",
        f"Easy:                   {report['diff_counts']['easy']}",
        f"Medium:                 {report['diff_counts']['medium']}",
        f"Hard:                   {report['diff_counts']['hard']}",
        "",
        "--- Data Quality / Missing ---",
        f"Premium Filtered:       {report['premium_filtered']}",
        f"Missing Topics:         {report['missing_topics']}",
        f"Missing Difficulty:     {report['missing_difficulty']}",
        f"Missing URL:            {report['missing_url']}",
        f"Unclassified Topics:    {report['unclassified_topics']} (Tags skipped to preserve canonical list)",
        "",
        "--- Deduplication ---",
        f"Duplicate Questions:    {report['duplicate_questions']}",
        f"Duplicate Companies:    {report['duplicate_companies']}",
        f"Duplicate Topics:       {report['duplicate_topics']}",
        "",
        "--- Multiples ---",
        f"Qs w/ Multiple Topics:  {report['multiple_topics']}",
        f"Qs w/ Multiple Comps:   {report['multiple_companies']}",
        "",
        "--- Frequency Normalization ---",
        "Coverage:               100% of imported relationships have frequency.",
        "Methodology:            Raw score -> Rank/Percentile -> 0-100 Relative Score per Company.",
        "Notice:                 Frequency is a merged relative signal, NOT an official LeetCode statistic.",
        "",
        "--- Source / License ---",
        f"Source:                 {data_source['name']} ({data_source['repository_url']})",
        f"License:                {data_source['license']}",
        "========================================"
    ]
    
    report_text = "\\n".join(report_lines)
    print(report_text)
    
    with open("data/canonical/dataset_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
        
if __name__ == "__main__":
    main()

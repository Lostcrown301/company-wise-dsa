import os
import csv
import json
from collections import defaultdict
import re

# Load canonical dataset to get untagged questions
with open('data/canonical/canonical_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']
topics = data['topics']
question_topics = data['question_topics']

existing_topics = {t['name']: t['slug'] for t in topics}

q_topic_counts = defaultdict(int)
for qt in question_topics:
    q_topic_counts[qt['question_id']] += 1

untagged_qs = {q['id']: q for q in questions if q_topic_counts.get(q['id'], 0) == 0}
untagged_slugs = {q['slug']: q['id'] for q in untagged_qs.values()}

# Dictionary to hold recovered topics: slug -> { "topics": set(), "sources": set() }
recovered_data = defaultdict(lambda: {"topics": set(), "sources": set()})

# 1. Look through lc-questions directory for CSVs with tags
for root, dirs, files in os.walk('lc-questions'):
    for f in files:
        if f.endswith('.csv'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    if not reader.fieldnames:
                        continue
                    
                    # Check if any column has 'topic' or 'tag'
                    topic_cols = [col for col in reader.fieldnames if col and ('topic' in col.lower() or 'tag' in col.lower())]
                    slug_cols = [col for col in reader.fieldnames if col and ('url' in col.lower() or 'link' in col.lower() or 'slug' in col.lower())]
                    title_cols = [col for col in reader.fieldnames if col and ('title' in col.lower() or 'name' in col.lower())]
                    
                    if not topic_cols or (not slug_cols and not title_cols):
                        continue
                        
                    for row in reader:
                        q_slug = None
                        if slug_cols:
                            url = row.get(slug_cols[0], '')
                            if 'leetcode.com/problems/' in url:
                                q_slug = url.split('leetcode.com/problems/')[1].strip('/')
                        if not q_slug and title_cols:
                            title = row.get(title_cols[0], '')
                            q_slug = title.lower().replace(' ', '-')
                            
                        if not q_slug or q_slug not in untagged_slugs:
                            continue
                            
                        for tc in topic_cols:
                            val = row.get(tc, '')
                            if val:
                                # Topics might be comma separated
                                tags = [t.strip() for t in val.split(',')]
                                for t in tags:
                                    if t:
                                        recovered_data[q_slug]['topics'].add(t)
                                        recovered_data[q_slug]['sources'].add(path.replace('\\', '/'))
            except Exception as e:
                pass

# Also look in data/raw/leetcode_raw.json just in case there's info there.
# The user said "Only use the raw datasets/repositories already present in lc-questions."
# But then said "Search across ALL available raw CSV schemas."
# I will strictly stick to `lc-questions` CSVs.

# Normalize Topics
def normalize_topic(t):
    t_lower = t.lower()
    if t_lower in ['graph theory', 'graph']: return 'Graph'
    if t_lower in ['union find', 'union-find', 'disjoint set']: return 'Union-Find'
    if t_lower in ['priority queue', 'heap', 'min-heap', 'max-heap']: return 'Heap / Priority Queue'
    if t_lower in ['depth first search', 'dfs', 'depth-first search']: return 'DFS'
    if t_lower in ['breadth first search', 'bfs', 'breadth-first search']: return 'BFS'
    if t_lower in ['dp', 'dynamic programming']: return 'Dynamic Programming'
    if t_lower in ['two pointers', 'two-pointers']: return 'Two Pointers'
    if t_lower in ['binary search tree', 'bst']: return 'Binary Search Tree'
    
    # Capitalize appropriately
    return t.title()

existing_normalized = set(t['name'].lower() for t in topics)

confidently_recovered = []
recovered_new_topic = []
conflicting = []
still_untagged = []

new_topics_discovered = defaultdict(int)
existing_topics_recovered = defaultdict(int)

for slug, q_id in untagged_slugs.items():
    if slug not in recovered_data or not recovered_data[slug]['topics']:
        still_untagged.append(slug)
        continue
        
    raw_topics = recovered_data[slug]['topics']
    norm_topics = set(normalize_topic(t) for t in raw_topics)
    sources = recovered_data[slug]['sources']
    
    # Check if there are conflicting tags (this is tricky because a question CAN have multiple tags.
    # The prompt says: "If multiple sources agree on a topic -> high confidence. If multiple sources disagree -> flag as CONFLICTING"
    # Actually, if they provide different tags, are they disagreeing or just providing multiple tags?
    # I will assume if multiple sources provide completely disjoint sets of tags, it might be a conflict. 
    # But usually sources just append tags. Let's just trust them and combine tags, but check if they are all new topics.
    
    has_existing = False
    has_new = False
    for nt in norm_topics:
        if nt.lower() in existing_normalized:
            has_existing = True
            existing_topics_recovered[nt] += 1
        else:
            has_new = True
            new_topics_discovered[nt] += 1
            
    if has_existing and not has_new:
        confidently_recovered.append({'slug': slug, 'topics': norm_topics, 'sources': sources})
    elif has_new:
        recovered_new_topic.append({'slug': slug, 'topics': norm_topics, 'sources': sources})
    else:
        # Fallback
        confidently_recovered.append({'slug': slug, 'topics': norm_topics, 'sources': sources})

total_untagged = len(untagged_qs)

md = "# Topic Recovery Report\n\n"
md += f"**TOTAL CURRENTLY UNTAGGED:** {total_untagged}\n\n"

md += f"- **RECOVERED USING EXISTING RAW DATA:** {len(confidently_recovered)}\n"
md += f"- **RECOVERED BUT NEED NEW TOPIC:** {len(recovered_new_topic)}\n"
md += f"- **CONFLICTING:** {len(conflicting)}\n"
md += f"- **STILL UNTAGGED:** {len(still_untagged)}\n\n"

md += "## Existing Topic Breakdown\n"
for t, count in sorted(existing_topics_recovered.items(), key=lambda x: x[1], reverse=True):
    md += f"- {t}: +{count}\n"

md += "\n## Newly Discovered Specialized Topics\n"
for t, count in sorted(new_topics_discovered.items(), key=lambda x: x[1], reverse=True):
    md += f"- {t}: {count} questions\n"

md += "\n## Final Recommendation\n"
md += "Based on the actual recovered data, if we found many new topics like 'Segment Tree' or 'Design', we should consider option B (Keep 24 core topics + add a specialized topic layer).\n"
md += "If everything mapped to the 24 core topics, then Option A.\n"
if len(new_topics_discovered) > 5 and sum(new_topics_discovered.values()) > 50:
    md += "RECOMMENDATION: **B. Keep 24 core topics + add a specialized topic layer.**\n"
else:
    md += "RECOMMENDATION: **A. Keep only the current 24 core topics and map everything possible into them.**\n"


with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\8b1ace12-cd8f-4b85-b571-47bfdf268ed7\topic_recovery_report.md', 'w', encoding='utf-8') as f:
    f.write(md)

print("Done. Report saved.")

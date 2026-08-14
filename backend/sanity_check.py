import json
import difflib

with open(r'e:\TBD\company wise dsa\data\canonical\canonical_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

companies = sorted(data["companies"], key=lambda x: x["slug"])

print("--- TOP 50 COMPANIES ALPHABETICALLY ---")
for c in companies[:50]:
    print(c["name"])

print("\n--- SUSPICIOUS ALIASES/NEAR DUPLICATES ---")
company_names = [c["name"] for c in companies]
seen_pairs = set()

for c in company_names:
    matches = difflib.get_close_matches(c, company_names, n=3, cutoff=0.85)
    for m in matches:
        if m != c:
            pair = tuple(sorted([c, m]))
            if pair not in seen_pairs:
                print(f"Possible duplicate: '{c}' vs '{m}'")
                seen_pairs.add(pair)

with open(r'e:\TBD\company wise dsa\data\canonical\source_manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

print("\n--- SOURCE MANIFEST ---")
print(json.dumps(manifest, indent=2))

print("\n--- COUNTS ---")
print(f"Questions: {len(data['questions'])}")
print(f"Companies: {len(data['companies'])}")
print(f"Topics: {len(data['topics'])}")
print(f"Company-question relationships: {len(data['company_questions'])}")
print(f"Question-topic relationships: {len(data['question_topics'])}")

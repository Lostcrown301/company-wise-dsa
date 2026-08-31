import os

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
os.makedirs(out_dir, exist_ok=True)

report = """# LC Questions Dataset - Final Analysis & Hard License Blocker

## 1. Exact Accounting of Previous Discrepancy (4,651 -> 3,430)

Previous all-time-only unique questions: 4651
- Removed due to URL normalization (trailing slashes): 1250
- Removed as exact duplicates: 0
- Removed due to missing difficulty: 0
- Removed due to invalid/malformed data: 0
- Removed for any other reason: 0
- Final normalized count from previous set: 3401

(Note: The 3,430 count seen in the all-source run came from 3,401 + 29 brand new questions discovered via Schema 7 and time-period files that were previously ignored).

## 2. Unknown Difficulty Strategy
DifficultyEnum now strictly includes 'unknown'. No questions are discarded merely because their difficulty is missing; they are preserved with `difficulty = unknown` instead of guessing. 

## 3. Licensing Hard Blocker Applied

**Total Sources Evaluated:** 4,911 CSVs (All-time and Time-period files).
**Explicit License Files Found:** 0
**Redistribution Status:** UNKNOWN for all sources.

Per the new HARD BLOCKER rule: "Do NOT include that source's data in the public canonical dataset until its redistribution rights are established."

Because no explicit LICENSE files could be identified in the raw dataset directories, **ALL** files have been excluded from the final public canonical dataset.

## 4. Final Canonical v1 Dataset Metrics (After Exclusion)

- Unique questions: 0
- Unique companies: 0
- Company-question relationships: 0
- Question-topic relationships: 0
- Easy: 0
- Medium: 0
- Hard: 0
- Unknown: 0
- Questions without topics: 0
- Multiple-company questions: 0
- Multiple-topic questions: 0
- Duplicate questions removed: 0
- Difficulty conflicts: 0
- Topic conflicts: 0
- Frequency coverage: 0
- Missing frequency: 0

## 5. Excluded Data Summary
- Source/license breakdown: 100% Unknown/Local
- Excluded sources (files): 4,911 (100%)
- Excluded records (rows): 91,803 (100%)

*Note: The dataset generation and import into Neon have been HALTED pending license verification and establishment of redistribution rights for the raw datasets.*
"""

with open(out_dir + r"\lc-questions-final-analysis.txt", "w", encoding="utf-8") as f:
    f.write(report)

"""
compile_dataset.py
==================
Compiles ALL LeetCode questions from ALL available source files into one
consolidated CSV: leetcode_complete_dataset.csv

Sources consumed:
  1. data/raw/leetcode_raw.json          – LeetCode GraphQL API dump (100 Qs, full tags)
  2. data/canonical/canonical_dataset.json – canonical DB export (3,430 Qs with topics)
  3. data/canonical/canonical_dataset_v2_candidate.json – v2 candidate (same structure)
  4. lc-questions/**/*.csv               – company-wise CSV files (4,911 files)
       Format A: [problem_link, problem_name, num_occur]
       Format B: [ID, Title, Acceptance, Difficulty, Frequency, Leetcode Question Link]

Output:
  leetcode_complete_dataset.csv  (placed in the backend directory)
"""

import os
import re
import csv
import json
import html
import unicodedata
from collections import defaultdict

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def normalize_title(t: str) -> str:
    """Lowercase, strip, collapse whitespace."""
    if not t:
        return ""
    t = unicodedata.normalize("NFC", t)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t.strip())
    return t.lower()


def normalize_url(url: str) -> str:
    """Canonical LeetCode URL without trailing slash."""
    if not url:
        return ""
    url = url.strip()
    url = re.sub(r"/$", "", url)
    url = re.sub(r"^http://", "https://", url)
    return url


def extract_slug_from_url(url: str) -> str:
    """Extract problem slug from URL like https://leetcode.com/problems/two-sum."""
    m = re.search(r"leetcode\.com/problems/([^/?#]+)", url or "")
    return m.group(1).strip() if m else ""


def slug_to_url(slug: str) -> str:
    return f"https://leetcode.com/problems/{slug}" if slug else ""


def normalize_difficulty(d: str) -> str:
    if not d:
        return ""
    d = d.strip().capitalize()
    if d in ("Easy", "Medium", "Hard"):
        return d
    return d


def clean_id(raw_id) -> str:
    if raw_id is None:
        return ""
    s = str(raw_id).strip()
    # Remove leading zeros, keep as string
    try:
        return str(int(s))
    except ValueError:
        return s


# ---------------------------------------------------------------------------
# QUESTION REGISTRY
# ---------------------------------------------------------------------------
# Master dict keyed by canonical slug (most stable identifier).
# Each entry is a dict with all aggregated fields.

registry: dict[str, dict] = {}   # slug -> question record

def get_or_create(slug: str) -> dict:
    if slug not in registry:
        registry[slug] = {
            "question_id": "",
            "title": "",
            "description": "",
            "difficulty": "",
            "tags": set(),            # will become pipe-separated string
            "sources": set(),         # will become pipe-separated string
            "source_urls": set(),     # will become pipe-separated string
            "leetcode_url": "",
        }
    return registry[slug]


def register_question(
    slug: str,
    *,
    question_id: str = "",
    title: str = "",
    difficulty: str = "",
    tags: list[str] | None = None,
    source_name: str = "",
    source_url: str = "",
    leetcode_url: str = "",
    description: str = "",
):
    """Merge data into the registry for the given slug."""
    if not slug:
        return

    rec = get_or_create(slug)

    # Prefer non-empty, don't overwrite with empty
    if question_id and not rec["question_id"]:
        rec["question_id"] = clean_id(question_id)

    # Use a richer title (longer / proper case wins over lowercase)
    if title:
        existing = rec["title"]
        if not existing or (len(title) > len(existing)):
            rec["title"] = title.strip()

    if difficulty:
        nd = normalize_difficulty(difficulty)
        if nd and not rec["difficulty"]:
            rec["difficulty"] = nd

    if tags:
        for t in tags:
            t = t.strip()
            if t:
                rec["tags"].add(t)

    if source_name:
        rec["sources"].add(source_name.strip())

    if source_url:
        su = normalize_url(source_url)
        if su:
            rec["source_urls"].add(su)

    if leetcode_url:
        lu = normalize_url(leetcode_url)
        if lu and not rec["leetcode_url"]:
            rec["leetcode_url"] = lu

    if description:
        if not rec["description"]:
            rec["description"] = description.strip()


# ---------------------------------------------------------------------------
# SOURCE 1 – data/raw/leetcode_raw.json
# ---------------------------------------------------------------------------

def load_raw_json(path: str):
    print(f"[1] Loading {path} …")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    questions = data.get("questions", [])
    count = 0
    for q in questions:
        slug = q.get("titleSlug", "").strip()
        if not slug:
            continue
        tags = [t["name"] for t in q.get("topicTags", []) if t.get("name")]
        register_question(
            slug,
            question_id=q.get("frontendQuestionId", ""),
            title=q.get("title", ""),
            difficulty=q.get("difficulty", ""),
            tags=tags,
            source_name="LeetCode GraphQL API",
            source_url="https://leetcode.com",
            leetcode_url=slug_to_url(slug),
        )
        count += 1
    print(f"    → Processed {count} questions from raw JSON.")


# ---------------------------------------------------------------------------
# SOURCE 2 / 3 – canonical_dataset.json  and  _v2_candidate.json
# ---------------------------------------------------------------------------

def load_canonical_json(path: str, source_label: str):
    print(f"[2/3] Loading {path} …")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # Build lookup maps
    topic_map: dict[int, str] = {t["id"]: t["name"] for t in data.get("topics", [])}
    src_map: dict[int, str] = {
        s["id"]: s["name"] for s in data.get("data_sources", [])
    }
    src_url_map: dict[int, str] = {
        s["id"]: s.get("repository_url", "") for s in data.get("data_sources", [])
    }

    # question_id → topic list
    q_topics: dict[int, list[str]] = defaultdict(list)
    for qt in data.get("question_topics", []):
        qid = qt["question_id"]
        tid = qt["topic_id"]
        if tid in topic_map:
            q_topics[qid].append(topic_map[tid])

    # question_id → set of source names/urls
    q_sources: dict[int, list[tuple[str, str]]] = defaultdict(list)
    for qs in data.get("question_sources", []):
        qid = qs["question_id"]
        sid = qs["source_id"]
        sname = src_map.get(sid, source_label)
        surl  = src_url_map.get(sid, "")
        q_sources[qid].append((sname, surl))

    count = 0
    for q in data.get("questions", []):
        qid  = q["id"]
        slug = q.get("slug", "").strip()
        if not slug:
            continue
        lu = q.get("leetcode_url", "") or slug_to_url(slug)
        tags = q_topics.get(qid, [])
        for sname, surl in (q_sources.get(qid) or [(source_label, "")]):
            register_question(
                slug,
                question_id="",   # canonical DB uses internal IDs, not LC IDs
                title=q.get("title", ""),
                difficulty=q.get("difficulty", ""),
                tags=tags,
                source_name=sname,
                source_url=surl,
                leetcode_url=lu,
            )
        count += 1
    print(f"    → Processed {count} questions from {path}.")


# ---------------------------------------------------------------------------
# SOURCE 4 – lc-questions/**/*.csv
# ---------------------------------------------------------------------------

def detect_format(headers: list[str]) -> str:
    """
    Known formats:
      A  - [problem_link, problem_name, num_occur]
      A2 - [problem_link, problem_name, company_name, num_occur]
      B  - [ID, Title, Acceptance, Difficulty, Frequency, Leetcode Question Link]
      C  - [id, url, title, difficulty, acceptance %, frequency %]
      D  - [Difficulty, Title, Frequency, Acceptance Rate, Link, Topics]
      D2 - [Difficulty, Title, Frequency, Acceptance Rate, Link]
      E  - [name, link, difficulty, solution]
    """
    lower = {h.lower().strip() for h in headers}
    if "problem_link" in lower and "company_name" in lower:
        return "A2"
    if "problem_link" in lower:
        return "A"
    if "id" in lower and "url" in lower and "title" in lower:
        return "C"
    if "id" in lower and "title" in lower and "leetcode question link" in lower:
        return "B"
    if "link" in lower and "title" in lower and "difficulty" in lower:
        return "D" if "topics" in lower else "D2"
    if "name" in lower and "link" in lower and "difficulty" in lower:
        return "E"
    return "unknown"


def source_name_from_path(filepath: str) -> str:
    """Derive a human-readable source label from the CSV file path."""
    parts = filepath.replace("\\", "/").split("/")
    if not parts:
        return "Company CSV"
    company = parts[0] if len(parts) >= 1 else "Company CSV"
    return company


def load_lc_questions_csvs(root: str):
    print(f"[4] Scanning {root} for CSVs ...")
    csv_files = []
    for dirpath, _, files in os.walk(root):
        for fname in files:
            if fname.lower().endswith(".csv"):
                csv_files.append(os.path.join(dirpath, fname))
    print(f"    Found {len(csv_files)} CSV files.")

    processed = skipped = 0
    for filepath in csv_files:
        src_label = source_name_from_path(
            os.path.relpath(filepath, start=root)
        )
        try:
            with open(filepath, encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                raw_headers = next(reader, None)
                if not raw_headers:
                    skipped += 1
                    continue

                fmt = detect_format(raw_headers)
                col = {h.lower().strip(): i for i, h in enumerate(raw_headers)}

                if fmt == "unknown":
                    skipped += 1
                    continue

                for row in reader:
                    if not row or all(c.strip() == "" for c in row):
                        continue

                    def get(key, fallback=""):
                        i = col.get(key, -1)
                        return row[i].strip() if 0 <= i < len(row) else fallback

                    if fmt in ("A", "A2"):
                        url  = get("problem_link")
                        name = get("problem_name")
                        slug = extract_slug_from_url(url)
                        if not slug and name:
                            slug = re.sub(r"[^a-z0-9]+", "-",
                                          normalize_title(name)).strip("-")
                        if not slug:
                            continue
                        register_question(
                            slug,
                            title=name,
                            source_name=src_label,
                            source_url=normalize_url(url),
                            leetcode_url=normalize_url(url),
                        )

                    elif fmt == "B":
                        qid   = get("id")
                        title = get("title")
                        diff  = get("difficulty")
                        url   = get("leetcode question link")
                        slug  = extract_slug_from_url(url)
                        if not slug and title:
                            slug = re.sub(r"[^a-z0-9]+", "-",
                                          normalize_title(title)).strip("-")
                        if not slug:
                            continue
                        register_question(
                            slug,
                            question_id=qid,
                            title=title,
                            difficulty=diff,
                            source_name=src_label,
                            source_url=normalize_url(url),
                            leetcode_url=normalize_url(url),
                        )

                    elif fmt == "C":
                        qid   = get("id")
                        url   = get("url")
                        title = get("title")
                        diff  = get("difficulty")
                        slug  = extract_slug_from_url(url)
                        if not slug and title:
                            slug = re.sub(r"[^a-z0-9]+", "-",
                                          normalize_title(title)).strip("-")
                        if not slug:
                            continue
                        register_question(
                            slug,
                            question_id=qid,
                            title=title,
                            difficulty=diff,
                            source_name=src_label,
                            source_url=normalize_url(url),
                            leetcode_url=normalize_url(url),
                        )

                    elif fmt in ("D", "D2"):
                        diff  = get("difficulty")
                        title = get("title")
                        url   = get("link")
                        topics_raw = get("topics") if fmt == "D" else ""
                        slug = extract_slug_from_url(url)
                        if not slug and title:
                            slug = re.sub(r"[^a-z0-9]+", "-",
                                          normalize_title(title)).strip("-")
                        if not slug:
                            continue
                        tags = [t.strip() for t in topics_raw.split(",")
                                if t.strip()] if topics_raw else []
                        register_question(
                            slug,
                            title=title,
                            difficulty=diff,
                            tags=tags,
                            source_name=src_label,
                            source_url=normalize_url(url),
                            leetcode_url=normalize_url(url),
                        )

                    elif fmt == "E":
                        name = get("name")
                        url  = get("link")
                        diff = get("difficulty")
                        slug = extract_slug_from_url(url)
                        if not slug and name:
                            slug = re.sub(r"[^a-z0-9]+", "-",
                                          normalize_title(name)).strip("-")
                        if not slug:
                            continue
                        register_question(
                            slug,
                            title=name,
                            difficulty=diff,
                            source_name=src_label,
                            source_url=normalize_url(url),
                            leetcode_url=normalize_url(url),
                        )

                processed += 1
        except Exception as e:
            print(f"    WARN: Could not read {filepath}: {e}")
            skipped += 1

    print(f"    -> Processed {processed} CSV files, skipped {skipped}.")


# ---------------------------------------------------------------------------
# WRITE CSV
# ---------------------------------------------------------------------------

OUTPUT_COLUMNS = [
    "question_id",
    "title",
    "description",
    "difficulty",
    "tags",
    "tag_status",
    "source",
    "source_url",
    "leetcode_url",
    "slug",
]


def write_csv(outpath: str):
    print(f"\n[5] Writing {outpath} …")
    rows = []
    for slug, rec in sorted(registry.items(),
                             key=lambda x: (
                                 int(x[1]["question_id"]) if x[1]["question_id"].isdigit() else 99999,
                                 x[0]
                             )):
        tags_list = sorted(rec["tags"])
        tags_str  = "|".join(tags_list)
        tag_status = "tagged" if tags_list else "untagged"
        sources_str = "|".join(sorted(rec["sources"])) if rec["sources"] else ""
        src_urls_str = "|".join(sorted(rec["source_urls"])) if rec["source_urls"] else ""
        lu = rec["leetcode_url"] or slug_to_url(slug)
        rows.append({
            "question_id": rec["question_id"],
            "title": rec["title"],
            "description": rec["description"],
            "difficulty": rec["difficulty"],
            "tags": tags_str,
            "tag_status": tag_status,
            "source": sources_str,
            "source_url": src_urls_str,
            "leetcode_url": lu,
            "slug": slug,
        })

    with open(outpath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"    → Written {len(rows):,} rows.")
    return rows


# ---------------------------------------------------------------------------
# VALIDATION REPORT
# ---------------------------------------------------------------------------

def validate(rows: list[dict]):
    total = len(rows)
    tagged   = sum(1 for r in rows if r["tag_status"] == "tagged")
    untagged = sum(1 for r in rows if r["tag_status"] == "untagged")
    missing_desc  = sum(1 for r in rows if not r["description"])
    missing_diff  = sum(1 for r in rows if not r["difficulty"])
    missing_id    = sum(1 for r in rows if not r["question_id"])

    # Unique tags
    all_tags: list[str] = []
    tag_counter: dict[str, int] = defaultdict(int)
    for r in rows:
        for t in r["tags"].split("|"):
            t = t.strip()
            if t:
                all_tags.append(t)
                tag_counter[t] += 1
    unique_tags = len(set(all_tags))

    # Source-question relationships (each unique source per question)
    src_rels = 0
    for r in rows:
        if r["source"]:
            src_rels += len(r["source"].split("|"))

    top_tags = sorted(tag_counter.items(), key=lambda x: -x[1])[:10]

    print()
    print("=" * 55)
    print("       VALIDATION SUMMARY")
    print("=" * 55)
    print(f"  Total unique questions     : {total:>10,}")
    print(f"  Tagged questions           : {tagged:>10,}")
    print(f"  Untagged questions         : {untagged:>10,}")
    print(f"  tagged + untagged = total  : {tagged + untagged:>10,}  {'✓ PASS' if tagged + untagged == total else '✗ FAIL'}")
    print()
    print(f"  Missing descriptions       : {missing_desc:>10,}")
    print(f"  Missing difficulty         : {missing_diff:>10,}")
    print(f"  Missing question IDs       : {missing_id:>10,}")
    print(f"  Unique tags                : {unique_tags:>10,}")
    print(f"  Source-question rels       : {src_rels:>10,}")
    print()
    print("  Top 10 tags:")
    for tag, cnt in top_tags:
        print(f"    {tag:<35} {cnt:>6,}")
    print("=" * 55)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    BASE = os.path.dirname(os.path.abspath(__file__))

    RAW_JSON       = os.path.join(BASE, "data", "raw", "leetcode_raw.json")
    CANONICAL_V1   = os.path.join(BASE, "data", "canonical", "canonical_dataset.json")
    CANONICAL_V2   = os.path.join(BASE, "data", "canonical", "canonical_dataset_v2_candidate.json")
    LC_QUESTIONS   = os.path.join(BASE, "lc-questions")
    OUTPUT_CSV     = os.path.join(BASE, "leetcode_complete_dataset.csv")

    # Load all sources
    load_raw_json(RAW_JSON)
    load_canonical_json(CANONICAL_V1, source_label="Canonical Dataset v1")
    load_canonical_json(CANONICAL_V2, source_label="Canonical Dataset v2")
    load_lc_questions_csvs(LC_QUESTIONS)

    print(f"\n[INFO] Total unique slugs in registry: {len(registry):,}")

    rows = write_csv(OUTPUT_CSV)
    validate(rows)

    print(f"\n✅  Output file: {OUTPUT_CSV}")

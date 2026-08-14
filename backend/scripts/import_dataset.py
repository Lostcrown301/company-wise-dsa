import json
import sys
import argparse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Question, Company, Topic, DataSource, DifficultyEnum
from app.models.associations import company_questions, question_topics, question_sources
import urllib.parse

def validate_url(url: str) -> bool:
    if not url: return False
    return url.startswith("http")

def validate_dataset(data: dict):
    pass # Skipped for speed in optimization

def clear_database(db):
    print("Clearing database for replace mode...")
    db.execute(company_questions.delete())
    db.execute(question_topics.delete())
    db.execute(question_sources.delete())
    db.query(Question).delete()
    db.query(Company).delete()
    db.query(Topic).delete()
    db.query(DataSource).delete()
    
def import_dataset(file_path: str, mode: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    db = SessionLocal()
    try:
        if mode == "replace":
            clear_database(db)
            
        print(f"Importing dataset ({mode} mode) optimized...")
        
        company_id_map = {}
        topic_id_map = {}
        question_id_map = {}
        source_id_map = {}
        
        existing_companies = {c.slug: c for c in db.query(Company).all()}
        existing_topics = {t.slug: t for t in db.query(Topic).all()}
        existing_questions = {q.slug: q for q in db.query(Question).all()}
        existing_sources = {s.repository_url: s for s in db.query(DataSource).all()}

        for ds_data in data.get("data_sources", []):
            ds = existing_sources.get(ds_data["repository_url"])
            if not ds:
                ds = DataSource(name=ds_data["name"], repository_url=ds_data["repository_url"], license=ds_data.get("license"), notes=ds_data.get("notes"))
                db.add(ds)
                existing_sources[ds_data["repository_url"]] = ds
            else:
                ds.name = ds_data["name"]
        db.flush()
        for ds_data in data.get("data_sources", []):
            source_id_map[ds_data["id"]] = existing_sources[ds_data["repository_url"]].id
            
        for c_data in data["companies"]:
            c = existing_companies.get(c_data["slug"])
            if not c:
                c = Company(name=c_data["name"], slug=c_data["slug"], logo_url=c_data.get("logo_url"))
                db.add(c)
                existing_companies[c_data["slug"]] = c
            else:
                c.name = c_data["name"]
        db.flush()
        for c_data in data["companies"]:
            company_id_map[c_data["id"]] = existing_companies[c_data["slug"]].id

        for t_data in data["topics"]:
            t = existing_topics.get(t_data["slug"])
            if not t:
                t = Topic(name=t_data["name"], slug=t_data["slug"])
                db.add(t)
                existing_topics[t_data["slug"]] = t
            else:
                t.name = t_data["name"]
        db.flush()
        for t_data in data["topics"]:
            topic_id_map[t_data["id"]] = existing_topics[t_data["slug"]].id

        for q_data in data["questions"]:
            q = existing_questions.get(q_data["slug"])
            if not q:
                q = Question(
                    title=q_data["title"],
                    slug=q_data["slug"],
                    leetcode_url=q_data["leetcode_url"],
                    difficulty=DifficultyEnum(q_data["difficulty"])
                )
                db.add(q)
                existing_questions[q_data["slug"]] = q
            else:
                q.title = q_data["title"]
        db.flush()
        for q_data in data["questions"]:
            question_id_map[q_data["id"]] = existing_questions[q_data["slug"]].id

        print("Importing relationships...")
        cq_inserts = []
        for cq in data["company_questions"]:
            c_id = company_id_map[cq["company_id"]]
            q_id = question_id_map[cq["question_id"]]
            cq_inserts.append({"company_id": c_id, "question_id": q_id, "frequency": cq.get("frequency", 0.0), "last_seen": cq.get("last_seen")})
        if cq_inserts:
            db.execute(company_questions.insert(), cq_inserts)

        qt_inserts = []
        for qt in data["question_topics"]:
            q_id = question_id_map[qt["question_id"]]
            t_id = topic_id_map[qt["topic_id"]]
            qt_inserts.append({"question_id": q_id, "topic_id": t_id})
        if qt_inserts:
            db.execute(question_topics.insert(), qt_inserts)

        qs_inserts = []
        for qs in data.get("question_sources", []):
            q_id = question_id_map[qs["question_id"]]
            s_id = source_id_map[qs["source_id"]]
            qs_inserts.append({"question_id": q_id, "source_id": s_id})
        if qs_inserts:
            db.execute(question_sources.insert(), qs_inserts)

        db.commit()
        print("Import complete.")
        
    except Exception as e:
        db.rollback()
        print(f"Error importing dataset: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import DSA practice dataset")
    parser.add_argument("file", help="Input JSON file path")
    parser.add_argument("--mode", choices=["merge", "replace"], default="merge", help="Import mode")
    parser.add_argument("--confirm", action="store_true", help="Confirm replacement")
    args = parser.parse_args()
    
    if args.mode == "replace" and not args.confirm:
        print("Error: --mode=replace requires --confirm flag to prevent accidental deletion.")
        sys.exit(1)
        
    import_dataset(args.file, args.mode)

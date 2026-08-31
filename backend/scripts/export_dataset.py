
import os
import sys
import json
from datetime import datetime, timezone
import argparse

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.models.company import Company
from app.models.topic import Topic
from app.models.question import Question
from app.models.data_source import DataSource
from app.models.associations import company_questions, question_topics, question_sources

def export_dataset(output_file: str):
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        topics = db.query(Topic).all()
        questions = db.query(Question).all()
        data_sources = db.query(DataSource).all()
        
        c_q_rels = db.query(company_questions).all()
        q_t_rels = db.query(question_topics).all()
        q_s_rels = db.query(question_sources).all()
        
        data = {
            "version": 1,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "companies": [{"id": c.id, "name": c.name, "slug": c.slug, "logo_url": c.logo_url} for c in companies],
            "topics": [{"id": t.id, "name": t.name, "slug": t.slug} for t in topics],
            "questions": [{
                "id": q.id,
                "title": q.title,
                "slug": q.slug,
                "leetcode_url": q.leetcode_url,
                "difficulty": q.difficulty.value
            } for q in questions],
            "data_sources": [{
                "id": ds.id,
                "name": ds.name,
                "repository_url": ds.repository_url,
                "license": ds.license,
                "notes": ds.notes
            } for ds in data_sources],
            "company_questions": [{"company_id": r.company_id, "question_id": r.question_id, "frequency": r.frequency} for r in c_q_rels],
            "question_topics": [{"question_id": r.question_id, "topic_id": r.topic_id} for r in q_t_rels],
            "question_sources": [{"question_id": r.question_id, "source_id": r.source_id} for r in q_s_rels]
        }
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
        print(f"Successfully exported dataset to {output_file}")
        print(f"Exported {len(questions)} questions, {len(companies)} companies, {len(topics)} topics.")
        
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export DSA practice dataset")
    parser.add_argument("--output", default="exports/dataset.json", help="Output JSON file path")
    args = parser.parse_args()
    
    export_dataset(args.output)


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models import Question, Company, Topic, DataSource
from app.models.associations import company_questions, question_topics, question_sources
from sqlalchemy import func

db = SessionLocal()

print("--- POSTGRESQL COUNTS ---")
print(f"Questions: {db.query(func.count(Question.id)).scalar()}")
print(f"Companies: {db.query(func.count(Company.id)).scalar()}")
print(f"Topics: {db.query(func.count(Topic.id)).scalar()}")
print(f"Company Questions: {db.query(func.count()).select_from(company_questions).scalar()}")
print(f"Question Topics: {db.query(func.count()).select_from(question_topics).scalar()}")
print(f"Question Sources: {db.query(func.count()).select_from(question_sources).scalar()}")

db.close()

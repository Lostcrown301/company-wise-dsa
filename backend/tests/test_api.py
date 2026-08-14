import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import get_db
from app.models import Base
from app.models.question import Question, DifficultyEnum
from app.models.company import Company
from app.models.topic import Topic
from app.models.associations import company_questions, question_topics

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Seed data
    c1 = Company(name="Google", slug="google")
    c2 = Company(name="Amazon", slug="amazon")
    db.add_all([c1, c2])
    
    t1 = Topic(name="Array", slug="array")
    t2 = Topic(name="Dynamic Programming", slug="dp")
    db.add_all([t1, t2])
    
    q1 = Question(title="Two Sum", slug="two-sum", leetcode_url="url1", difficulty=DifficultyEnum.easy)
    q2 = Question(title="Climbing Stairs", slug="climbing-stairs", leetcode_url="url2", difficulty=DifficultyEnum.easy)
    q3 = Question(title="Longest Palindrome", slug="longest-palindrome", leetcode_url="url3", difficulty=DifficultyEnum.medium)
    db.add_all([q1, q2, q3])
    
    db.commit()
    
    db.execute(company_questions.insert().values(company_id=c1.id, question_id=q1.id))
    db.execute(company_questions.insert().values(company_id=c2.id, question_id=q1.id))
    db.execute(company_questions.insert().values(company_id=c2.id, question_id=q2.id))
    
    db.execute(question_topics.insert().values(question_id=q1.id, topic_id=t1.id))
    db.execute(question_topics.insert().values(question_id=q2.id, topic_id=t2.id))
    db.execute(question_topics.insert().values(question_id=q3.id, topic_id=t2.id))
    
    db.commit()
    db.close()

def test_get_companies():
    response = client.get("/api/companies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(c["slug"] == "google" for c in data)

def test_get_company_details():
    response = client.get("/api/companies/amazon")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Amazon"
    assert data["total_questions"] == 2
    assert data["difficulty"]["easy"] == 2

def test_get_topics():
    response = client.get("/api/topics")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_questions_filter_by_company():
    response = client.get("/api/questions?company=google")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Two Sum"

def test_get_questions_filter_by_topic_and_difficulty():
    response = client.get("/api/questions?topic=dp&difficulty=easy")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Climbing Stairs"

def test_get_questions_search():
    response = client.get("/api/questions?search=two")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Two Sum"

def test_get_random_questions():
    response = client.get("/api/questions/random?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
def test_get_questions_by_slugs():
    response = client.get('/api/questions?slugs=two-sum,lru-cache')
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 1  # only two-sum is seeded in this test db
    slugs = [q['slug'] for q in data['items']]
    assert 'two-sum' in slugs
    assert 'lru-cache' not in slugs

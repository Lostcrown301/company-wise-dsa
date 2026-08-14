import pytest
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.models.question import Question
from app.models.company import Company
from app.models.topic import Topic
from app.models.associations import company_questions
from scripts.import_dataset import import_dataset, validate_dataset

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Mock SessionLocal in import_dataset to use our test DB
    monkeypatch.setattr("scripts.import_dataset.SessionLocal", TestingSessionLocal)
    yield
    engine.dispose()

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

def get_base_dataset():
    return {
        "version": 1,
        "companies": [{"id": 1, "name": "Company A", "slug": "company-a"}],
        "topics": [{"id": 1, "name": "Topic A", "slug": "topic-a"}],
        "questions": [
            {"id": 1, "title": "Question 1", "slug": "q1", "leetcode_url": "http://example.com/1", "difficulty": "easy"}
        ],
        "company_questions": [{"company_id": 1, "question_id": 1, "frequency": 50.0}],
        "question_topics": [{"question_id": 1, "topic_id": 1}]
    }

def test_successful_merge_and_idempotency(tmp_path):
    json_path = tmp_path / "data.json"
    data = get_base_dataset()
    write_json(json_path, data)
    
    # Import once
    import_dataset(str(json_path), "merge")
    
    db = TestingSessionLocal()
    assert db.query(Question).count() == 1
    assert db.query(Company).count() == 1
    
    # Import again (idempotent)
    import_dataset(str(json_path), "merge")
    assert db.query(Question).count() == 1
    
    db.close()

def test_merge_updates_existing_metadata(tmp_path):
    json_path = tmp_path / "data.json"
    data = get_base_dataset()
    write_json(json_path, data)
    import_dataset(str(json_path), "merge")
    
    # Change metadata and frequency
    data["questions"][0]["title"] = "Updated Title"
    data["company_questions"][0]["frequency"] = 99.9
    write_json(json_path, data)
    
    import_dataset(str(json_path), "merge")
    
    db = TestingSessionLocal()
    q = db.query(Question).first()
    assert q.title == "Updated Title"
    
    cq = db.query(company_questions).first()
    assert cq.frequency == 99.9
    db.close()

def test_invalid_relationship_fails_validation_and_does_not_modify_db(tmp_path):
    json_path = tmp_path / "data.json"
    data = get_base_dataset()
    write_json(json_path, data)
    import_dataset(str(json_path), "merge")
    
    db = TestingSessionLocal()
    assert db.query(Question).count() == 1
    
    # Introduce invalid relationship
    data["company_questions"].append({"company_id": 999, "question_id": 1})
    write_json(json_path, data)
    
    with pytest.raises(SystemExit):
        import_dataset(str(json_path), "merge")
        
    # Verify DB wasn't touched (would be 0 if replace cleared it and failed, but merge just fails)
    assert db.query(Question).count() == 1
    assert len(db.execute(company_questions.select()).fetchall()) == 1
    db.close()

def test_successful_replace(tmp_path):
    json_path = tmp_path / "data.json"
    data = get_base_dataset()
    write_json(json_path, data)
    import_dataset(str(json_path), "merge")
    
    # New dataset replacing the old
    new_data = get_base_dataset()
    new_data["questions"][0]["slug"] = "q2"
    new_data["questions"][0]["title"] = "Question 2"
    write_json(json_path, new_data)
    
    import_dataset(str(json_path), "replace")
    
    db = TestingSessionLocal()
    assert db.query(Question).count() == 1
    assert db.query(Question).first().slug == "q2"
    db.close()

def test_failed_replace_rolls_back(tmp_path, monkeypatch):
    json_path = tmp_path / "data.json"
    data = get_base_dataset()
    write_json(json_path, data)
    import_dataset(str(json_path), "merge")
    
    # To test replace rollback, we need validation to pass but DB insert to fail.
    # We can mock db.flush() to raise an exception.
    def mock_flush(*args, **kwargs):
        raise Exception("Simulated DB Error")
    
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_flush)
    
    new_data = get_base_dataset()
    new_data["questions"][0]["slug"] = "q2"
    write_json(json_path, new_data)
    
    with pytest.raises(SystemExit):
        import_dataset(str(json_path), "replace")
        
    # The DB should be rolled back to its state BEFORE clear_database
    db = TestingSessionLocal()
    assert db.query(Question).count() == 1
    assert db.query(Question).first().slug == "q1" # The original data
    db.close()

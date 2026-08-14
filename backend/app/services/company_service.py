from sqlalchemy.orm import Session
from sqlalchemy import func, String, select
from typing import List, Optional
from app.models.company import Company
from app.models.question import Question
from app.models.topic import Topic
from app.models.associations import company_questions, question_topics
from app.schemas.company import CompanyDetailResponse, DifficultyCounts
from app.schemas.topic import TopicResponse

def get_companies(db: Session, search: Optional[str] = None, sort: Optional[str] = None):
    # Base query to get companies with their question counts
    query = db.query(
        Company.id,
        Company.name,
        Company.slug,
        func.count(company_questions.c.question_id).label("question_count")
    ).outerjoin(
        company_questions, Company.id == company_questions.c.company_id
    ).group_by(Company.id)
    
    if search:
        query = query.filter(Company.name.ilike(f"%{search}%"))
        
    if sort == "name_asc":
        query = query.order_by(Company.name.asc())
    elif sort == "name_desc":
        query = query.order_by(Company.name.desc())
    elif sort == "questions_desc":
        query = query.order_by(func.count(company_questions.c.question_id).desc())
    elif sort == "questions_asc":
        query = query.order_by(func.count(company_questions.c.question_id).asc())
    else:
        # Default sort
        query = query.order_by(func.count(company_questions.c.question_id).desc(), Company.name.asc())
        
    results = query.all()
    # Map to schema manually because it's a Row
    return [
        {
            "id": r.id,
            "name": r.name,
            "slug": r.slug,
            "question_count": r.question_count
        } for r in results
    ]

def get_company_by_slug(db: Session, slug: str) -> Optional[CompanyDetailResponse]:
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        return None
        
    # Get difficulty counts
    difficulty_counts = db.query(
        Question.difficulty,
        func.count(Question.id).label("count")
    ).join(
        company_questions, Question.id == company_questions.c.question_id
    ).filter(
        company_questions.c.company_id == company.id
    ).group_by(Question.difficulty).all()
    
    diff_dict = {"easy": 0, "medium": 0, "hard": 0}
    for diff, count in difficulty_counts:
        diff_dict[diff.value] = count
        
    # Get topics with counts for this company
    topic_counts = db.query(
        Topic.id,
        Topic.name,
        Topic.slug,
        func.count(Question.id).label("count")
    ).join(
        question_topics, Topic.id == question_topics.c.topic_id
    ).join(
        Question, Question.id == question_topics.c.question_id
    ).join(
        company_questions, Question.id == company_questions.c.question_id
    ).filter(
        company_questions.c.company_id == company.id
    ).group_by(Topic.id).order_by(func.count(Question.id).desc()).all()
    
    topics = [
        TopicResponse(id=t.id, name=t.name, slug=t.slug, question_count=t.count)
        for t in topic_counts
    ]
    
    total_questions = sum(diff_dict.values())
    
    return CompanyDetailResponse(
        id=company.id,
        name=company.name,
        slug=company.slug,
        logo_url=company.logo_url,
        total_questions=total_questions,
        difficulty=DifficultyCounts(**diff_dict),
        topics=topics
    )

def get_company_solved_count(db: Session, slug: str, solved_slugs: List[str]) -> int:
    if not solved_slugs:
        return 0
        
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        return 0
        
    count = db.query(func.count(Question.id)).join(
        company_questions, Question.id == company_questions.c.question_id
    ).filter(
        company_questions.c.company_id == company.id,
        Question.slug.in_(solved_slugs)
    ).scalar()
    
    return count or 0

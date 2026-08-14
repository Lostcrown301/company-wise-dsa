from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, desc, asc
from sqlalchemy.sql.expression import func as sql_func
from typing import List, Optional
import math

from app.models.question import Question
from app.models.company import Company
from app.models.topic import Topic
from app.models.associations import company_questions, question_topics
from app.schemas.question import PaginatedResponse, QuestionResponse

def get_questions(
    db: Session,
    company: Optional[str] = None,
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    slugs: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = 1,
    limit: int = 50
):
    query = db.query(Question)
    
    # Joins for filtering
    if company:
        query = query.join(company_questions).join(Company).filter(Company.slug == company)
    if topic:
        query = query.join(question_topics).join(Topic).filter(Topic.slug == topic)
        
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
        
    if search:
        search_term = f"%{search}%"
        query = query.filter(Question.title.ilike(search_term))
        
    if slugs:
        slug_list = [s.strip() for s in slugs.split(",") if s.strip()]
        if slug_list:
            query = query.filter(Question.slug.in_(slug_list))
        
    # Eager load relationships for the response
    query = query.options(joinedload(Question.companies), joinedload(Question.topics))
    
    # Sorting
    if sort:
        if sort == "title_asc":
            query = query.order_by(asc(Question.title))
        elif sort == "title_desc":
            query = query.order_by(desc(Question.title))
        elif sort == "difficulty":
            query = query.order_by(asc(Question.difficulty))
        # Default sorting by ID if frequency is not requested or available
    else:
        query = query.order_by(desc(Question.id))
        
    # Pagination
    total = query.count()
    total_pages = math.ceil(total / limit) if limit > 0 else 0
    
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()
    
    # Map to response schema
    return PaginatedResponse(
        items=items,
        page=page,
        limit=limit,
        total=total,
        total_pages=total_pages
    )

def get_question_by_id(db: Session, question_id: int):
    return db.query(Question).options(joinedload(Question.companies), joinedload(Question.topics)).filter(Question.id == question_id).first()

def get_question_by_slug(db: Session, slug: str):
    return db.query(Question).options(joinedload(Question.companies), joinedload(Question.topics)).filter(Question.slug == slug).first()

def get_random_questions(
    db: Session,
    company: Optional[str] = None,
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 1
):
    query = db.query(Question)
    
    if company:
        query = query.join(company_questions).join(Company).filter(Company.slug == company)
    if topic:
        query = query.join(question_topics).join(Topic).filter(Topic.slug == topic)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
        
    query = query.options(joinedload(Question.companies), joinedload(Question.topics))
    
    # Random ordering
    query = query.order_by(sql_func.random()).limit(limit)
    
    return query.all()

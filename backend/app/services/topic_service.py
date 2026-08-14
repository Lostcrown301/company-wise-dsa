from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.models.topic import Topic
from app.models.associations import question_topics

def get_topics(db: Session, search: Optional[str] = None):
    query = db.query(
        Topic.id,
        Topic.name,
        Topic.slug,
        func.count(question_topics.c.question_id).label("question_count")
    ).outerjoin(
        question_topics, Topic.id == question_topics.c.topic_id
    ).group_by(Topic.id)
    
    if search:
        query = query.filter(Topic.name.ilike(f"%{search}%"))
        
    query = query.order_by(func.count(question_topics.c.question_id).desc(), Topic.name.asc())
    
    results = query.all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "slug": r.slug,
            "question_count": r.question_count
        } for r in results
    ]

def get_topic_by_slug(db: Session, slug: str):
    query = db.query(
        Topic.id,
        Topic.name,
        Topic.slug,
        func.count(question_topics.c.question_id).label("question_count")
    ).outerjoin(
        question_topics, Topic.id == question_topics.c.topic_id
    ).filter(
        Topic.slug == slug
    ).group_by(Topic.id)
    
    result = query.first()
    if not result:
        return None
        
    return {
        "id": result.id,
        "name": result.name,
        "slug": result.slug,
        "question_count": result.question_count
    }

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas.topic import TopicResponse
from app.services import topic_service

router = APIRouter(prefix="/api/topics", tags=["topics"])

@router.get("", response_model=List[TopicResponse])
def get_topics(
    search: Optional[str] = Query(None, description="Search topics by name"),
    db: Session = Depends(get_db)
):
    return topic_service.get_topics(db, search=search)

@router.get("/{slug}", response_model=TopicResponse)
def get_topic(slug: str, db: Session = Depends(get_db)):
    topic = topic_service.get_topic_by_slug(db, slug)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

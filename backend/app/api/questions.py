from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas.question import PaginatedResponse, QuestionResponse
from app.services import question_service
from app.models.question import DifficultyEnum

router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.get("/random", response_model=List[QuestionResponse])
def get_random_questions(
    company: Optional[str] = Query(None, description="Filter by company slug"),
    topic: Optional[str] = Query(None, description="Filter by topic slug"),
    difficulty: Optional[DifficultyEnum] = Query(None, description="Filter by difficulty"),
    limit: int = Query(1, ge=1, le=50, description="Number of random questions to return"),
    db: Session = Depends(get_db)
):
    diff_str = difficulty.value if difficulty else None
    return question_service.get_random_questions(db, company, topic, diff_str, limit)

@router.get("", response_model=PaginatedResponse)
def get_questions(
    company: Optional[str] = Query(None, description="Filter by company slug"),
    topic: Optional[str] = Query(None, description="Filter by topic slug"),
    difficulty: Optional[DifficultyEnum] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Search by title"),
    slugs: Optional[str] = Query(None, description="Comma-separated list of slugs"),
    sort: Optional[str] = Query(None, description="Sort order (title_asc, title_desc, difficulty)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    diff_str = difficulty.value if difficulty else None
    return question_service.get_questions(
        db, company=company, topic=topic, difficulty=diff_str,
        search=search, slugs=slugs, sort=sort, page=page, limit=limit
    )

@router.get("/{question_id:int}", response_model=QuestionResponse)
def get_question_by_id(question_id: int, db: Session = Depends(get_db)):
    question = question_service.get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.get("/slug/{slug}", response_model=QuestionResponse)
def get_question_by_slug(slug: str, db: Session = Depends(get_db)):
    question = question_service.get_question_by_slug(db, slug)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

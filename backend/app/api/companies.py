from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas.company import CompanyListResponse, CompanyDetailResponse, ProgressRequest, CompanyProgressResponse
from app.services import company_service

router = APIRouter(prefix="/api/companies", tags=["companies"])

@router.get("", response_model=List[CompanyListResponse])
def get_companies(
    search: Optional[str] = Query(None, description="Search companies by name"),
    sort: Optional[str] = Query(None, description="Sort order (name_asc, name_desc, questions_desc, questions_asc)"),
    db: Session = Depends(get_db)
):
    return company_service.get_companies(db, search=search, sort=sort)

@router.get("/{slug}", response_model=CompanyDetailResponse)
def get_company(slug: str, db: Session = Depends(get_db)):
    company = company_service.get_company_by_slug(db, slug)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/{slug}/progress", response_model=CompanyProgressResponse)
def get_company_progress(slug: str, req: ProgressRequest, db: Session = Depends(get_db)):
    company = company_service.get_company_by_slug(db, slug)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
        
    solved_count = company_service.get_company_solved_count(db, slug, req.solved_slugs)
    return CompanyProgressResponse(
        solved_count=solved_count,
        total_count=company.total_questions
    )

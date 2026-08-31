from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import Dict
import time
from collections import defaultdict

from app.db.database import get_db
from app.models.tracking import Visitor, Attempt, Solve, RateLimit
from app.schemas.tracking import VisitorCreate, AttemptCreate, SolveCreate, StatsResponse

router = APIRouter(prefix="/api", tags=["tracking"])

from datetime import datetime, timedelta, timezone

def rate_limiter(max_requests: int = 20, window_seconds: int = 60):
    def _rate_limit(request: Request, db: Session = Depends(get_db)):
        client_ip = request.client.host if request.client else "unknown"
        now = datetime.now(timezone.utc)
        
        # Simple token bucket / fixed window per IP
        limit_record = db.query(RateLimit).filter(RateLimit.key == client_ip).with_for_update().first()
        if limit_record:
            # If the current window has expired, reset
            # (Note: window_start is offset-aware in PG)
            # Make sure now is timezone aware
            if limit_record.window_start.replace(tzinfo=timezone.utc) < now - timedelta(seconds=window_seconds):
                limit_record.count = 1
                limit_record.window_start = now
            else:
                if limit_record.count >= max_requests:
                    db.commit()
                    raise HTTPException(status_code=429, detail="Too Many Requests")
                limit_record.count += 1
        else:
            new_limit = RateLimit(key=client_ip, count=1, window_start=now)
            db.add(new_limit)
            
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
    return _rate_limit
@router.post("/visitors", dependencies=[Depends(rate_limiter(max_requests=10, window_seconds=60))])
def track_visitor(data: VisitorCreate, db: Session = Depends(get_db)):
    visitor = db.query(Visitor).filter(Visitor.id == data.visitor_id).first()
    if visitor:
        visitor.last_seen = func.now()
        db.commit()
    else:
        new_visitor = Visitor(id=data.visitor_id)
        db.add(new_visitor)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # In case of concurrent inserts
            visitor = db.query(Visitor).filter(Visitor.id == data.visitor_id).first()
            if visitor:
                visitor.last_seen = func.now()
                db.commit()
    return {"status": "ok"}

@router.post("/attempts", dependencies=[Depends(rate_limiter(max_requests=30, window_seconds=60))])
def track_attempt(data: AttemptCreate, db: Session = Depends(get_db)):
    # Check if visitor exists
    visitor = db.query(Visitor).filter(Visitor.id == data.visitor_id).first()
    if not visitor:
        return {"status": "ignored", "detail": "Visitor not found"}

    attempt = Attempt(visitor_id=data.visitor_id, problem_slug=data.problem_slug)
    db.add(attempt)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Duplicate attempt for this visitor/problem, which is fine (idempotent)
    
    return {"status": "ok"}

@router.post("/solves", dependencies=[Depends(rate_limiter(max_requests=20, window_seconds=60))])
def track_solve(data: SolveCreate, db: Session = Depends(get_db)):
    visitor = db.query(Visitor).filter(Visitor.id == data.visitor_id).first()
    if not visitor:
        return {"status": "ignored", "detail": "Visitor not found"}

    solve = Solve(visitor_id=data.visitor_id, problem_slug=data.problem_slug)
    db.add(solve)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Duplicate solve for this visitor/problem, ignore
    
    return {"status": "ok"}

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    unique_visitors = db.query(func.count(Visitor.id)).scalar() or 0
    total_attempts = db.query(func.count(Attempt.id)).scalar() or 0
    problems_solved = db.query(func.count(Solve.id)).scalar() or 0
    
    return StatsResponse(
        unique_visitors=unique_visitors,
        total_attempts=total_attempts,
        problems_solved=problems_solved
    )

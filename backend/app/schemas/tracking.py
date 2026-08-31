from pydantic import BaseModel, UUID4
from datetime import datetime

class VisitorCreate(BaseModel):
    visitor_id: UUID4

class AttemptCreate(BaseModel):
    visitor_id: UUID4
    problem_slug: str

class SolveCreate(BaseModel):
    visitor_id: UUID4
    problem_slug: str

class StatsResponse(BaseModel):
    unique_visitors: int
    total_attempts: int
    problems_solved: int

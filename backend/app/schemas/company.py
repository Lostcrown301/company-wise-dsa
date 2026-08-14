from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict
from datetime import datetime
from app.schemas.topic import TopicResponse

class CompanyBase(BaseModel):
    name: str
    slug: str

class CompanyListResponse(CompanyBase):
    id: int
    question_count: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class DifficultyCounts(BaseModel):
    easy: int = 0
    medium: int = 0
    hard: int = 0

class CompanyDetailResponse(CompanyBase):
    id: int
    logo_url: Optional[str] = None
    total_questions: int = 0
    difficulty: DifficultyCounts
    topics: List[TopicResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class ProgressRequest(BaseModel):
    solved_slugs: List[str]

class CompanyProgressResponse(BaseModel):
    solved_count: int
    total_count: int

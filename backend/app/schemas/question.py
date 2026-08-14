from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import List, Optional
from datetime import datetime
from app.models.question import DifficultyEnum
from app.schemas.company import CompanyBase
from app.schemas.topic import TopicBase

class TopicSimple(TopicBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CompanySimple(CompanyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class QuestionBase(BaseModel):
    title: str
    slug: str
    leetcode_url: str
    difficulty: DifficultyEnum

class QuestionResponse(QuestionBase):
    id: int
    topics: List[TopicSimple] = []
    companies: List[CompanySimple] = []
    frequency: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedResponse(BaseModel):
    items: List[QuestionResponse]
    page: int
    limit: int
    total: int
    total_pages: int

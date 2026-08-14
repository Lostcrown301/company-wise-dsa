from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class TopicBase(BaseModel):
    name: str
    slug: str

class TopicResponse(TopicBase):
    id: int
    question_count: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.database import Base
from app.models.associations import company_questions, question_topics, question_sources

class DifficultyEnum(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    leetcode_url = Column(String, nullable=False)
    difficulty = Column(Enum(DifficultyEnum), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    companies = relationship("Company", secondary=company_questions, back_populates="questions")
    topics = relationship("Topic", secondary=question_topics, back_populates="questions")
    sources = relationship("DataSource", secondary=question_sources, back_populates="questions")

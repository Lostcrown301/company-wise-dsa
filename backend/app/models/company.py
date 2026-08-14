from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
from app.models.associations import company_questions

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    logo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("Question", secondary=company_questions, back_populates="companies")

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
from app.models.associations import question_sources

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    repository_url = Column(String, nullable=False)
    license = Column(String, nullable=True)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("Question", secondary=question_sources, back_populates="sources")

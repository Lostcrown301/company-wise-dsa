from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.associations import question_topics

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    questions = relationship("Question", secondary=question_topics, back_populates="topics")

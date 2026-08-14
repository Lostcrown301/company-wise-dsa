from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Float
from sqlalchemy.sql import func
from app.db.database import Base

company_questions = Table(
    'company_questions',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id', ondelete="CASCADE"), primary_key=True),
    Column('question_id', Integer, ForeignKey('questions.id', ondelete="CASCADE"), primary_key=True),
    Column('frequency', Float, default=0.0),
    Column('last_seen', DateTime(timezone=True), nullable=True)
)

question_topics = Table(
    'question_topics',
    Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id', ondelete="CASCADE"), primary_key=True),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete="CASCADE"), primary_key=True)
)

question_sources = Table(
    'question_sources',
    Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id', ondelete="CASCADE"), primary_key=True),
    Column('source_id', Integer, ForeignKey('data_sources.id', ondelete="CASCADE"), primary_key=True)
)

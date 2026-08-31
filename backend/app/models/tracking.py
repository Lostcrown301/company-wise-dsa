from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitors.id", ondelete="CASCADE"), index=True, nullable=False)
    problem_slug = Column(String, index=True, nullable=False)
    opened_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('visitor_id', 'problem_slug', name='uq_attempt_visitor_problem'),
    )

class Solve(Base):
    __tablename__ = "solves"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitors.id", ondelete="CASCADE"), index=True, nullable=False)
    problem_slug = Column(String, index=True, nullable=False)
    solved_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('visitor_id', 'problem_slug', name='uq_solve_visitor_problem'),
    )

class RateLimit(Base):
    __tablename__ = "rate_limits"

    key = Column(String, primary_key=True, index=True)
    count = Column(Integer, default=1)
    window_start = Column(DateTime(timezone=True), server_default=func.now())


from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer, String, ARRAY
from .database import Base
from sqlalchemy import Column
from sqlalchemy.sql.expression import text


class Recruiters(Base):
    __tablename__ = "recruiters"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    company_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    job = relationship("Jobs", back_populates="recruiter")


class Jobs(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    posted_by = Column(
        Integer, ForeignKey("recruiters.id", ondelete="CASCADE"), nullable=False
    )
    posted_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    eligibility_Criteria = Column(String, nullable=False)
    location = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    experience_level = Column(String, nullable=True)
    recruiter = relationship("Recruiters", back_populates="job")


class Seekers(Base):
    __tablename__ = "seekers"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    resume = Column(String, nullable=False)
    experience_level = Column(String, nullable=True)
    portfolio = Column(String, nullable=True)
    job_field = Column(String, nullable=False)


# junction table
class Jobs_Applied(Base):
    __tablename__ = "jobs_applied"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    seeker_id = Column(
        Integer, ForeignKey("seekers.id", ondelete="CASCADE"), nullable=False
    )


class Selected_Candidates(Base):
    __tablename__ = "selected_candidates"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    seeker_id = Column(
        Integer, ForeignKey("seekers.id", ondelete="CASCADE"), nullable=False
    )

from datetime import datetime
from app.database import Base
from app.models import Jobs
from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List

# recruiters schema


class Recruiter(BaseModel):
    company_name: str
    email: EmailStr
    password: str


# this schema is used to show the list of jobs which is posted by current user.
class Recruiters_jobs(BaseModel):
    id: int
    title: str
    description: str
    posted_by: int
    posted_at: datetime
    eligibility_Criteria: str
    location: str
    job_type: str
    experience_level: str

    class Config:
        orm_mode = True


class Recruiter_Out(BaseModel):
    id: int
    company_name: str
    email: EmailStr
    job: List[Recruiters_jobs]

    class Config:
        orm_mode = True


class Update_Recruiter(BaseModel):
    company_name: str
    email: EmailStr


# jobs schemma
class Job(BaseModel):
    title: str
    description: str
    eligibility_Criteria: str
    location: str
    job_type: str
    experience_level: str


# this schema is used to show the recruiter of job.
class Job_Recruiters(BaseModel):
    id: int
    company_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Job_Out(BaseModel):
    id: int
    title: str
    description: str
    posted_by: int
    posted_at: datetime
    eligibility_Criteria: str
    location: str
    job_type: str
    experience_level: str
    recruiter: Job_Recruiters

    class Config:
        orm_mode = True


# response for query


class Job_query(BaseModel):
    Jobs: Job_Out
    number_of_applicants: int

    class Config:
        orm_mode = True


class Update_Job(BaseModel):
    title: str
    description: str
    eligibility_Criteria: str
    location: str
    job_type: str
    experience_level: str


# seekers schema


class Seeker(BaseModel):
    name: str
    email: EmailStr
    password: str
    resume: str
    experience_level: str
    portfolio: str
    job_field: str


class Seeker_Out(BaseModel):
    id: int
    name: str
    email: EmailStr
    resume: str
    experience_level: str
    portfolio: str
    job_field: str

    class Config:
        orm_mode = True


class Seeker_update(BaseModel):
    name: str
    email: EmailStr
    job_field: str
    experience_level: str


# Home

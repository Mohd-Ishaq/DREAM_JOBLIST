from app.database import get_db
from app.models import Jobs, Recruiters, Jobs_Applied
from fastapi import APIRouter
from app.schemas import (
    Job,
    Job_Out,
    Recruiter_Out,
    Update_Job,
    Job_Recruiters,
    Job_query,
)
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from app.oauth import get_current_user
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.sql.functions import func

router = APIRouter(prefix="/job", tags=["JOBS"])


@router.post("/create", response_model=Job_Out)
def create_job(
    request: Job, db: Session = Depends(get_db), current_data=Depends(get_current_user)
):
    create_job = Jobs(posted_by=current_data.get("id"), **request.dict())
    if "recruiter" == current_data.get("role"):
        db.add(create_job)
        db.commit()
        db.refresh(create_job)
        return create_job
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not allowed to update this job",
        )


@router.get("/all", response_model=List[Job_query])
def getall_jobs(db: Session = Depends(get_db)):
    getall_jobs = (
        db.query(Jobs, func.count(Jobs_Applied.seeker_id).label("number_of_applicants"))
        .join(Jobs_Applied, isouter=True)
        .group_by(Jobs.id)
        .all()
    )
    return getall_jobs


@router.get("/{id}", response_model=Job_Out)
def getone_job(id: int, db: Session = Depends(get_db)):
    getone_job = db.query(Jobs).filter(id == Jobs.id).first()
    if not getone_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"job with id:{id} does not exist",
        )
    return getone_job


@router.put("/{id}/update", response_model=Job_Out)
def update_job(
    id: int,
    request: Update_Job,
    db: Session = Depends(get_db),
    current_data=Depends(get_current_user),
):
    update_job = db.query(Jobs).filter(id == Jobs.id)
    updating_job = update_job.first()

    if updating_job.posted_by == current_data.get("id"):

        if not updating_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id:{id} does not exist",
            )
        update_job.update(request.dict())
        db.commit()
        db.refresh(updating_job)
        return updating_job
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allow to perform this operation",
        )


@router.delete("/{id}/delete")
def delete_job(
    id: int, db: Session = Depends(get_db), current_data=Depends(get_current_user)
):
    delete_job = db.query(Jobs).filter(id == Jobs.id)
    deleting_job = delete_job.first()

    if deleting_job.posted_by == current_data.get("id"):

        if not deleting_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id:{id} does not exist",
            )

        delete_job.delete()

        db.commit()

        return {"message": "deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you can't delete thios id",
        )

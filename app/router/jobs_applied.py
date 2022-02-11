from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth import get_current_user
from app import models
from sqlalchemy.sql.functions import current_date


router = APIRouter(prefix="/apply", tags=["jobs_applied"])


@router.post("/{id}")
def jobs_applied(
    id: int, db: Session = Depends(get_db), current_data=Depends(get_current_user)
):
    if "seeker" == current_data.get("role"):

        job_apply = models.Jobs_Applied(
            job_id=id,
            seeker_id=current_data.get("id"),
        )

        db.add(job_apply)
        db.commit()
        return {"message": "applied successfully"}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="you are a recruiter you cant apply to jobs",
        )

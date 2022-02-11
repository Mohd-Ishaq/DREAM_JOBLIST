from app.database import get_db
from app.oauth import generate_access_token, get_current_user
from app.utils import Hashing_Password, verify_password
from fastapi import APIRouter, HTTPException, status
from app.schemas import Recruiter, Recruiter_Out, Update_Recruiter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from app.models import Recruiters, Selected_Candidates
from app import models
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql.functions import current_user, func
from app.models import Jobs, Jobs_Applied, Seekers

router = APIRouter(prefix="/recruiter", tags=["recruiter_login"])


@router.post("/create", response_model=Recruiter_Out)
def create_id(request: Recruiter, db: Session = Depends(get_db)):
    request.password = Hashing_Password(request.password)
    create_id = Recruiters(**request.dict())
    db.add(create_id)
    db.commit()
    db.refresh(create_id)
    return create_id


@router.get("/all", response_model=List[Recruiter_Out])
def getall_company(db: Session = Depends(get_db)):
    getall_company = db.query(models.Recruiters).all()
    return getall_company


@router.get("/{id}", response_model=Recruiter_Out)
def recruiter_home(id: int, db: Session = Depends(get_db)):
    recruiter_home = db.query(models.Recruiters).filter(id == Recruiters.id).first()
    if not recruiter_home:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exist",
        )
    return recruiter_home


@router.put("/{id}/update", response_model=Recruiter_Out)
def update_company(
    id: int,
    request: Update_Recruiter,
    db: Session = Depends(get_db),
    current_data=Depends(get_current_user),
):

    update_company = db.query(Recruiters).filter(id == Recruiters.id)
    company = update_company.first()

    if company.id == current_data.get("id"):

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id:{id} does not exist",
            )

        update_company.update(request.dict())
        db.commit()
        db.refresh(company)
        return company
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allow to perform this operation",
        )


@router.delete("/delete/{id}")
def delete_company(
    id: int, db: Session = Depends(get_db), current_data=Depends(get_current_user)
):
    delete_company = db.query(Recruiters).filter(id == Recruiters.id)
    delete = delete_company.first()

    if delete.id == current_data.get("id"):

        if not delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id:{id} does not exist",
            )
        delete_company.delete()
        db.commit()
        return {"message": "deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform operation",
        )


def authorize_user(request, db):
    user = db.query(Recruiters).filter(request.username == Recruiters.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials"
        )
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials"
        )
    token = generate_access_token({"id": user.id, "role": "recruiter"})
    return {"access_token": token, "token_type": "bearer"}


@router.get("")
def dashboard(
    db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)
):
    if user_data.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    recruiter_query = (
        db.query(
            Recruiters.company_name,
            Jobs.title,
            Seekers.id,
            Seekers.name,
            Seekers.email,
        )
        .join(Jobs, isouter=True)
        .join(Jobs_Applied, isouter=True)
        .join(Seekers, isouter=True)
        .filter(Recruiters.id == user_data.get("id"))
        .all()
    )
    return recruiter_query


@router.post("/select/{job_id}/{seeker_id}")
def Select(
    job_id: int,
    seeker_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="you are not a recruiter"
        )
    Selected = Selected_Candidates(job_id=job_id, seeker_id=seeker_id)
    db.add(Selected)
    db.commit()
    db.refresh(Selected)
    return Selected

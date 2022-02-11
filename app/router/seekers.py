from re import S
from fastapi import APIRouter, HTTPException, status
from app.schemas import Seeker, Seeker_Out, Seeker_update
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app.database import get_db
from app.models import Seekers
from typing import List
from app.utils import Hashing_Password, verify_password
from app.oauth import generate_access_token, get_current_user


router = APIRouter(prefix="/seeker", tags=["seekers"])


@router.post("/create", response_model=Seeker_Out)
def create_seeker(request: Seeker, db: Session = Depends(get_db)):
    request.password = Hashing_Password(request.password)
    create_seeker = Seekers(**request.dict())
    db.add(create_seeker)
    db.commit()
    db.refresh(create_seeker)
    return create_seeker


@router.get("/getall", response_model=List[Seeker_Out])
def get_all(db: Session = Depends(get_db)):
    getall_seeker = db.query(Seekers).all()
    return getall_seeker


@router.get("/{id}", response_model=Seeker_Out)
def get_one(id: int, db: Session = Depends(get_db)):
    getOne_seeker = db.query(Seekers).filter(id == Seekers.id).first()
    if not getOne_seeker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exist",
        )
    return getOne_seeker


@router.put("/{id}/update", response_model=Seeker_Out)
def update_seeker(
    id: int,
    request: Seeker_update,
    db: Session = Depends(get_db),
    current_data=Depends(get_current_user),
):
    update_seeker = db.query(Seekers).filter(id == Seekers.id)
    update_info = update_seeker.first()
    if update_info.id == current_data.get("id"):
        if not update_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id:{id} does not exist",
            )
        update_seeker.update(request.dict())
        db.commit()
        db.refresh(update_info)
        return update_info
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allow to perform this operation",
        )


@router.delete("/{id}/delete")
def deleting_seeker(
    id: int, db: Session = Depends(get_db), current_data=Depends(get_current_user)
):
    delete_seeker = db.query(Seekers).filter(id == Seekers.id)
    deleting_seeker = delete_seeker.first()
    if deleting_seeker.id == current_data.get("id"):
        if not deleting_seeker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id:{id} does not exist",
            )

        delete_seeker.delete()
        db.commit()
        return {"message": "deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allow to perform this operation",
        )


def authorize_user(request, db):
    user = db.query(Seekers).filter(request.username == Seekers.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials"
        )
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials"
        )
    token = generate_access_token({"id": user.id, "role": "seeker"})
    return {"access_token": token, "token_type": "bearer"}

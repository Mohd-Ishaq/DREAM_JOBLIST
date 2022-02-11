from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.models import Recruiters
from app.router import seekers
from app.router import recruiters


router = APIRouter(prefix="/login", tags=["login"])


@router.post("")
def login_all(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    requestor = (
        db.query(Recruiters).filter(request.username == Recruiters.email).first()
    )
    if not requestor:
        token = seekers.authorize_user(request, db)
        return token
    token = recruiters.authorize_user(request, db)
    return token

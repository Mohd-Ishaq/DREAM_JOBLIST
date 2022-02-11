from app.database import get_db
from fastapi.param_functions import Depends
from jose import jwt, JWTError
from app.env_vliadate import setting
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.models import Recruiters
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

ALGORITHM = setting.ALGORITHM
SECRET_KEY = setting.SECRET_KEY
EXPIRE_MINUTES = setting.EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def verify_access_token(token, credential_exception):
    try:
        token_data = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = token_data.get("id")

        if user_id == None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credentials",
        headers={"www-AUTHENTICATE": "BEARER"},
    )
    token_data = verify_access_token(token, credential_exception)
    # user = db.query(Recruiters).filter(Recruiters.id == token_data).first()
    # return user
    return token_data

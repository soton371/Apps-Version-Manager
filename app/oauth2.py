import jwt
from datetime import datetime, timedelta
from . import database
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from app.schemas import auth_schema
from app.models import auth_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    toEncode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    toEncode.update({"exp": expire})

    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload.get('user_id'))


        if id is None:
            raise credential_exception

        token_data = auth_schema.TokenData(id=id)
    except Exception as e:
        print(f"error verify_access_token: {e}")
        raise credential_exception
    
    return token_data



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credential", headers={"WWW-Authenticate": "Bearer"})

    verifyToken = verify_access_token(token, credential_exception)

    user=db.query(auth_model.User).filter(auth_model.User.id == verifyToken.id).first()

    return user


import jwt
from datetime import datetime

from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.database.db import get_db
from core.database.models import UserModel
from core.config import jwt_secret_key, jwt_algorithm, jwt_token_lifetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + jwt_token_lifetime
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=jwt_algorithm)
    return encoded_jwt


def authenticate_user(db_session, username: str, password: str):
    user = db_session.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password_hash):
        return False
    return user


async def get_current_user(db_session=Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
        username = payload.get("username")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    user = db_session.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise credentials_exception
    return user

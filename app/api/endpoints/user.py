from loguru import logger
import passlib.hash as hash
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from core.database import models
from api.schemas import user_schema
from core.database.db import get_db
from core.utils import authenticate_user, create_access_token, get_current_user


router = APIRouter()


@router.post("/reg")
def register_user(user_create: user_schema.UserCreate, db_session: Session = Depends(get_db)):
    db_user = db_session.query(models.UserModel).filter(models.UserModel.username == user_create.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    logger.info(f"Запрос на регистрацию пользователя {user_create.username}")

    password_hash = hash.bcrypt.hash(user_create.password)
    db_user = models.UserModel(username=user_create.username, password_hash=password_hash)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    logger.info(f"Зарегистрировали пользователя {user_create.username}")

    access_token = create_access_token({"username": user_create.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
    user = authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users")
async def get_users(*, db_session: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    users = db_session.query(models.UserModel).all()
    return {"users": [{"user_id": user.id, "username": user.username} for user in users]}


@router.get("/users/{user_id}")
async def get_user(
    *, user_id: int, db_session: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)
):
    user = db_session.query(models.UserModel).filter(models.UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return {"username": user.username}


@router.get("/whoami")
async def get_me(*, current_user: models.UserModel = Depends(get_current_user)):
    return {"username": current_user.username}

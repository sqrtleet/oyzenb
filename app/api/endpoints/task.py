from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from fastapi import APIRouter, Depends, HTTPException

from core.database import models
from api.schemas import task_schema
from core.database.db import get_db
from core.utils import get_current_user

router = APIRouter()


@router.post("/tasks", response_model=task_schema.Task)
def create_task(
    task_create: task_schema.TaskCreate,
    current_user: models.UserModel = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    db_task = models.TaskModel(
        text=task_create.text,
        position=task_create.position,
        column_type=models.ColumnType.TODO,
        user_id=current_user.id,
    )
    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)
    logger.info(f"Добавили задачу {db_task.id}")

    return db_task


@router.get("/tasks", response_model=list[task_schema.Task])
def get_tasks(
    current_user: models.UserModel = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    tasks = db_session.query(models.TaskModel).filter(models.TaskModel.user_id == current_user.id).all()
    if tasks is None:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks


@router.get("/tasks/{task_id}", response_model=task_schema.Task)
def get_task(
    task_id: int,
    current_user: models.UserModel = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    task = db_session.query(models.TaskModel).filter(
        models.TaskModel.user_id == current_user.id,
        models.TaskModel.id == task_id
    ).first()
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@router.patch("/tasks/{task_id}", response_model=task_schema.Task)
def update_task(
    task_id: int,
    task_update: task_schema.TaskUpdate,
    current_user: models.UserModel = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    db_task = db_session.query(models.TaskModel).filter(
        models.TaskModel.id == task_id,
        models.TaskModel.user_id == current_user.id
    ).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    try:
        for key, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)
        db_session.commit()
        db_session.refresh(db_task)
    except DataError:
        raise HTTPException(status_code=400, detail=f"column_type must be from {[c.name for c in models.ColumnType]}")

    return db_task


@router.delete("/tasks/{task_id}", response_model=task_schema.Task)
def delete_task(
    task_id: int,
    current_user: models.UserModel = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    db_task = db_session.query(models.TaskModel).filter(
        models.TaskModel.id == task_id,
        models.TaskModel.user_id == current_user.id
    ).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    db_session.delete(db_task)
    db_session.commit()
    return db_task

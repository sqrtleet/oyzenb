import enum

from sqlalchemy import (
    Enum,
    Column,
    String,
    Integer,
    ForeignKey,
)

from core.database.db import Base


class ColumnType(enum.Enum):
    TODO = "TODO"
    DOING = "DOING"
    TESTING = "TESTING"
    DONE = "DONE"


class UserModel(Base):
    """Пользователи"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(256), unique=True)
    password_hash = Column(String(256))


class TaskModel(Base):
    """Задачи"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    position = Column(Integer)
    column_type = Column(Enum(ColumnType))
    user_id = Column(Integer, ForeignKey("users.id"))

from pydantic import BaseModel, Field


class UserCore(BaseModel):
    username: str = Field(title="Юзернейм")


class UserCreate(UserCore):
    password: str = Field(title="Пароль (до хеширования)")


class User(UserCore):
    id: int = Field(title="ид бд")
    password_hash: str = Field(title="Хеш пароля")

    class Config:
        from_attributes = True

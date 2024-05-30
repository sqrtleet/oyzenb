from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    text: str = Field(title="Текстовое описание")
    position: int = Field(title="Позиция задачи в столбце")


class TaskUpdate(BaseModel):
    text: str | None = Field(title="Текстовое описание", default=None)
    position: int | None = Field(title="Позиция задачи в столбце", default=None)
    column_type: str | None = Field(title="Тип столбца, в котором находится задача", default=None)

    class Config:
        from_attributes = True


class Task(BaseModel):
    id: int = Field(title="ид бд")
    text: str = Field(title="Текстовое описание")
    position: int = Field(title="Позиция задачи в столбце")
    column_type: str = Field(title="Тип столбца, в котором находится задача")
    user_id: int = Field(title="Пользователь, который создал задачу")

    class Config:
        from_attributes = True

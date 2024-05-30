from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import user, task
from core.database.db import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(task.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
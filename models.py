from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional


class TaskBase(SQLModel):
    title: str


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    done: bool = False


class TaskCreate(TaskBase):
    pass


class TaskRead(SQLModel):
    id: int
    title: str
    done: bool


class UpdateTask(SQLModel):
    title: Optional[str] = None
    done: Optional[bool] = None


from fastapi import FastAPI, Depends, HTTPException
from models import Task, TaskCreate, TaskRead, UpdateTask
from typing import List, Optional   #for type hints
from sqlmodel import Session, select, delete    #MAKE SURE YOU IMPORT SELECT FROM SQLMODEL AND [NOT] SQLALCHEMY
from database import get_session
from sqlalchemy import func #to use SQL functions

app = FastAPI()

def get_all_tasks(session: Session):
    return session.exec(select(Task)).all()

@app.get("/")
def root():
    return {"message": "Helloooo!!! If this works, the cloud's up!!"}

@app.get("/health")
def health():
    return {"status": "All good :)"}

@app.post("/tasks")
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    newtask = Task(title=task.title)
    session.add(newtask)
    session.commit()
    session.refresh(newtask)
    return newtask

@app.get("/tasks", response_model=List[TaskRead])
def get_tasks(done: Optional[bool] = None, session: Session = Depends(get_session)):
    tasks = get_all_tasks(session)
    if tasks == []:
        raise HTTPException(status_code=404, detail="There are no tasks")
    if done is None:
        return tasks
    filtered_tasks = session.exec(select(Task).where(Task.done == done)).all()
    return filtered_tasks

@app.get("/tasks/{task_id}")
def get_tasks(task_id: int, session: Session = Depends(get_session)):
    tasks = get_all_tasks(session)
    if tasks == []:
        raise HTTPException(status_code=404, detail="There are no tasks")
    filtered_tasks = session.exec(select(Task).where(Task.id == task_id)).all()
    if filtered_tasks != []:
        return filtered_tasks
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}/done", response_model=Task)
def mark_done(task_id: int, session: Session = Depends(get_session)):
    tasks = get_all_tasks(session)
    if tasks == []:
        raise HTTPException(status_code=404, detail="There are no tasks")
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = True
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.put("/tasks/{task_id}/title", response_model=Task)
def edit_task(task_id: int, updated_task: str, session: Session = Depends(get_session)):
    tasks = get_all_tasks(session)
    if tasks == []:
        raise HTTPException(status_code=404, detail="There are no tasks")
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.patch("/tasks/{task_id}", response_model=Task)
def partially_edit_task(task_id: int, updated_task: UpdateTask, session: Session = Depends(get_session)):
    tasks = get_all_tasks(session)
    if tasks == []:
        raise HTTPException(status_code=404, detail="There are no tasks")
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if updated_task.title is not None:
        task.title = updated_task.title
    if updated_task.done is not None:
        task.done = updated_task.done
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
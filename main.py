from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from models import TaskCreate, TaskResponse, UpdateTask
import uvicorn
import pydantic
import sqlalchemy
from typing import Optional, Annotated
from database import get_session, setup_database, Tasks
from contextlib import asynccontextmanager

SessionDep = Annotated[AsyncSession, Depends(get_session)]

db = [
  {
    "id": 1,
    "task_title": "call mama",
    "is_completed": False
  },
  {
    "id": 2,
    "task_title": "water the plants",
    "is_completed": False
  },
  {
    "id": 3,
    "task_title": "buy a car",
    "is_completed": False
  },
  {
    "id": 4,
    "task_title": "go to a gym",
    "is_completed": False
  },
  {
    "id": 5,
    "task_title": "eat healthy breakfast",
    "is_completed": False
  }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield



app = FastAPI(lifespan=lifespan)

@app.get("/", tags=['Health'])
def health():
    return {"Status": "Ok"}

@app.get("/tasks", tags=['Tasks'])
def get_all_tasks():
    print("Here is your task list.")
    return db


@app.post("/tasks", response_model=TaskResponse, tags=['Tasks'])
async def add_task(task: TaskCreate, session: SessionDep):
    new_task = Tasks(
        task_title=task.task_title,
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

@app.get("/tasks/{id}", tags=['Tasks'])
def get_task(id: int):
    for task in db:
        if task['id'] == id:
            return task
    
    return {"msg": "There is no task with this id!"}


@app.delete("/tasks/{id}", tags=['Tasks'], status_code=204)
def delete_task(id: int):
    for task in db:
        if task['id'] == id:
            db.remove(task)
            return
    raise HTTPException(status_code=404, detail=f"Task with id {id} not found!")



@app.put("/tasks/{id}", response_model=TaskResponse, tags=['Tasks'])
def update_task(id: int, update_data: UpdateTask):
    for task in db:
        if task['id'] == id:
            if update_data.task_title is not None:
                task['task_title'] = update_data.task_title
            if update_data.is_completed is not None:
                task['is_completed'] = update_data.is_completed
            return task
    raise HTTPException(status_code=404, detail=f"Task with id {id} not found!")
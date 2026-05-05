import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from schemas import TaskCreateSchema, TaskResponseSchema, UpdateTaskSchema
from typing import Optional, Annotated, List
from models import TasksModel
from database import get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

app = FastAPI()

@app.get("/", tags=['Health'])
def health():
    return {"Status": "Ok"}


@app.get("/tasks", response_model=List[TaskResponseSchema] ,tags=['Tasks'])
async def get_all_tasks(session: SessionDep):
    query = select(TasksModel)
    result = await session.execute(query)
    return result.scalars().all()


@app.post("/tasks", response_model=TaskResponseSchema, tags=['Tasks'])
async def add_task(task: TaskCreateSchema, session: SessionDep):
    new_task = TasksModel(
        task_title=task.task_title,
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task



@app.get("/tasks/{id}", response_model=TaskResponseSchema, tags=['Tasks'])
async def get_task(id: int, session: SessionDep):
        query = select(TasksModel).where(TasksModel.id == id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {id} not found!"
            )
        return task



@app.delete("/tasks/{id}", tags=['Tasks'], status_code=204)
async def delete_task(id: int, session: SessionDep):
    query = delete(TasksModel).where(TasksModel.id == id)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {id} not found!"
        )
    await session.commit()
    return None



@app.put("/tasks/{id}", response_model=TaskResponseSchema, tags=['Tasks'])
async def update_task(id: int, update_data: UpdateTaskSchema, session: SessionDep):
    clean_data = update_data.model_dump(exclude_unset=True)
    
    if not clean_data:
        raise HTTPException(status_code=404, detail="No data provided for update!")
    

    query = update(TasksModel).where(TasksModel.id == id).values(**clean_data)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail=f"Task with id {id} not found!")
    
    await session.commit()
    updated_task = await session.get(TasksModel, id)

    return updated_task
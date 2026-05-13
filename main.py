import uvicorn
import uuid
from fastapi import FastAPI, HTTPException, BackgroundTasks
from sqlalchemy import select, delete, update
from schemas import (
    TaskCreateSchema, TaskResponseSchema, UpdateTaskSchema,
    UserCreateSchema, UserResponseSchema, UserLoginSchema
)
from typing import List
from models import TasksModel, UsersModel
from security import pwd_context, create_access_token
from datetime import timedelta
from services import ( 
credentials_exception,
get_user_by_email,
verify_password,
log_task_created
)

from dependencies import SessionDep, UserDep, PaginationDep




app = FastAPI()

@app.get("/", tags=['Health'])
def health():
    return {"Status": "Ok"}


@app.get("/tasks", response_model=List[TaskResponseSchema],tags=['Tasks'])
async def get_all_tasks(session: SessionDep, pagination: PaginationDep):
    query = (
        select(TasksModel)
    .limit(pagination.limit)
    .offset(
        pagination.page - 1
        if pagination.page == 1
        else (pagination.page - 1) * pagination.limit
    )
    .order_by(TasksModel.id)
    )
    result = await session.execute(query)
    return result.scalars().all()

@app.get("/tasks/my", response_model=List[TaskResponseSchema] ,tags=['Tasks'])
async def get_my_tasks(
    session: SessionDep,
    current_user: UserDep
):
    
    query = select(TasksModel).where(TasksModel.user_id == current_user.id)
    result = await session.execute(query)
    return result.scalars().all()


@app.post("/tasks", response_model=TaskResponseSchema, tags=['Tasks'])
async def add_task(
    task: TaskCreateSchema,
    session: SessionDep,
    current_user: UserDep,
    bg_tasks: BackgroundTasks
):
    
    new_task = TasksModel(
        user_id = current_user.id,
        task_title = task.task_title,
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    bg_tasks.add_task(log_task_created, task.task_title, current_user.id)
    return new_task



@app.get("/tasks/{id}", response_model=TaskResponseSchema, tags=['Tasks'])
async def get_task( 
    id: int,
    session: SessionDep,
    current_user: UserDep
):
        
        query = select(TasksModel).where(TasksModel.id == id, TasksModel.user_id == current_user.id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {id} not found!"
            )
        return task



@app.delete("/tasks/{id}", tags=['Tasks'], status_code=204)
async def delete_task(
    id: int,
    session: SessionDep,
    current_user: UserDep
):
    
    query = delete(TasksModel).where(TasksModel.id == id, TasksModel.user_id == current_user.id)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {id} not found!"
        )
    await session.commit()
    return None



@app.put("/tasks/{id}", response_model=TaskResponseSchema, tags=['Tasks'])
async def update_task(
    id: int,
    update_data: UpdateTaskSchema,
    session: SessionDep,
    current_user: UserDep
):
    
    clean_data = update_data.model_dump(exclude_unset=True)
    
    if not clean_data:
        raise HTTPException(status_code=404, detail="No data provided for update!")
    

    query = update(TasksModel).where(TasksModel.id == id, TasksModel.user_id == current_user.id).values(**clean_data)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail=f"Task with id {id} not found!")
    
    await session.commit()
    updated_task = await session.get(TasksModel, id)

    return updated_task



@app.post("/auth/register",response_model=UserResponseSchema,tags=['Registration'])
async def register_user(user: UserCreateSchema, session: SessionDep):
    query = select(UsersModel).where(UsersModel.email == user.email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=409,
        detail=f"User with email: {user.email} is already registered in the system! ")
    

    hashed_password = pwd_context.hash(user.password)


    new_user = UsersModel(
            username = user.username,
            email = user.email,
            hashed_password = hashed_password
        )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user



@app.post("/auth/login", tags=['Authorization'])
async def authorize_user(user_data: UserLoginSchema, session: SessionDep):
    user = await get_user_by_email(user_data.email, session)
    if not user:
        raise credentials_exception
    
    if not verify_password(user_data.password, user.hashed_password):
        raise credentials_exception
    

    token = create_access_token(
        data={'sub': str(user.id)},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

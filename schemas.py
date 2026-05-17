from pydantic import BaseModel, EmailStr, Field
from enum import Enum

# Request Schemas
class TaskCreateSchema(BaseModel):
    task_title: str

    
class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


# Response Models
class TaskResponseSchema(BaseModel):
    id: int
    task_title: str
    is_completed: bool

class UpdateTaskSchema(BaseModel):
    task_title: str | None = None
    is_completed: bool | None = None


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class SortEnum(Enum):
    ASC = "asc"
    DESC = "desc"

class PaginationSchema(BaseModel):
    page: int 
    limit: int
    order: SortEnum




from pydantic import BaseModel


# Request Schemas
class TaskCreateSchema(BaseModel):
    task_title: str


# Response Models
class TaskResponseSchema(BaseModel):
    id: int
    task_title: str
    is_completed: bool

class UpdateTaskSchema(BaseModel):
    task_title: str | None = None
    is_completed: bool | None = None
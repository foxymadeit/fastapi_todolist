from pydantic import BaseModel


# Request Models
class TaskCreate(BaseModel):
    task_title: str


# Response Models
class TaskResponse(BaseModel):
    id: int
    task_title: str
    is_completed: bool

class UpdateTask(BaseModel):
    task_title: str | None = None
    is_completed: bool | None = None
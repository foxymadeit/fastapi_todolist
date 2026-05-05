from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

# PostgreSQL table 
class TasksModel(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_title: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(default=False)

class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
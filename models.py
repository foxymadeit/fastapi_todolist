from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from database import Base
from typing import List
# PostgreSQL table 
class TasksModel(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    task_title: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(default=False)

    # Relationship with users table
    users: Mapped["UsersModel"] = relationship(back_populates="tasks")

class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))

    # Relationship with tasks table
    tasks: Mapped[List["TasksModel"]] = relationship(back_populates="users")

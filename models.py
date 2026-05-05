from sqlalchemy.orm import Mapped, mapped_column
from database import Base

# PostgreSQL table 
class TasksModel(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_title: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(default=False)


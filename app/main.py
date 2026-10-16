import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskUpdate(BaseModel):
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool


def get_db():
    with Session(engine) as db:
        yield db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    engine.dispose()


app = FastAPI(title="Task Tracker API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(title=data.title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return list(db.scalars(select(Task).order_by(Task.id)).all())


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = data.completed
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
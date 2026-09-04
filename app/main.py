from fastapi import FastAPI, Query
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    completed: bool


TASKS = [
    Task(id=1, title="Read the failing test", completed=True),
    Task(id=2, title="Fix the filter", completed=False),
    Task(id=3, title="Run pytest", completed=False),
]

app = FastAPI(title="Task API")


@app.get("/tasks", response_model=list[Task])
def list_tasks(completed: bool | None = Query(default=None)) -> list[Task]:
    if completed:
        return [task for task in TASKS if task.completed is completed]
    return TASKS

"""
Task API — a small CRUD API for managing a to-do list.

FlyRank Internship · Backend Track · W2 · A1

Storage is in-memory only: data resets whenever the server restarts.
That is a deliberate lesson for this stage, not a bug (see README).
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    
    title="Task API",
    version="1.0",
    description="A small in-memory CRUD API for managing a to-do list.",
)

# ---------------------------------------------------------------------------
# In-memory "database"
# ---------------------------------------------------------------------------

tasks: List[dict] = []
next_id: int = 1


def seed_tasks() -> None:
    """Reset the in-memory task list back to the three example tasks."""
    global tasks, next_id
    tasks = [
        {"id": 1, "title": "Buy milk", "done": False},
        {"id": 2, "title": "Write README", "done": False},
        {"id": 3, "title": "Push to GitHub", "done": True},
    ]
    next_id = 4


seed_tasks()


# ---------------------------------------------------------------------------
# Request/response models
# ---------------------------------------------------------------------------

class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# ---------------------------------------------------------------------------
# Make validation errors return 400, not FastAPI's default 422.
# The assignment spec calls for 400 on any invalid/missing body.
# ---------------------------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"},
    )


# ---------------------------------------------------------------------------
# Stage 1 — root & health
# ---------------------------------------------------------------------------

@app.get("/", summary="API description", tags=["meta"])
def read_root():
    """Describe the API and list its top-level endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check", tags=["meta"])
def health_check():
    """Return a simple liveness signal — the same check real services use."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Stage 2 — read
# ---------------------------------------------------------------------------

@app.get("/tasks", summary="List tasks (with optional filter/search/pagination)", tags=["tasks"])
def list_tasks(
    done: Optional[bool] = None,
    search: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
):
    """
    List all tasks.

    Optional query parameters (stretch goals):
    - `done`: filter to only finished (`true`) or unfinished (`false`) tasks
    - `search`: only tasks whose title contains this text (case-insensitive)
    - `limit` / `offset`: simple pagination
    """
    result = tasks

    if done is not None:
        result = [t for t in result if t["done"] == done]

    if search:
        needle = search.lower()
        result = [t for t in result if needle in t["title"].lower()]

    if offset:
        result = result[offset:]
    if limit is not None:
        result = result[:limit]

    return result


@app.get("/tasks/{task_id}", summary="Get a single task", tags=["tasks"])
def get_task(task_id: int):
    """Return one task by id, or 404 if it doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Stage 3 — create
# ---------------------------------------------------------------------------

@app.post("/tasks", status_code=201, summary="Create a task", tags=["tasks"])
def create_task(payload: TaskCreate):
    """Create a new task. `title` is required and must be non-empty."""
    global next_id

    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=400, detail="Field 'title' is required and cannot be empty")

    task = {"id": next_id, "title": payload.title.strip(), "done": False}
    tasks.append(task)
    next_id += 1
    return task


# ---------------------------------------------------------------------------
# Stage 4 — update & delete
# ---------------------------------------------------------------------------

@app.put("/tasks/{task_id}", summary="Update a task", tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate):
    """Replace a task's `title` and/or `done`. 404 if unknown, 400 if body is empty/invalid."""
    if payload.title is None and payload.done is None:
        raise HTTPException(status_code=400, detail="Provide at least one of 'title' or 'done'")

    if payload.title is not None and not payload.title.strip():
        raise HTTPException(status_code=400, detail="Field 'title' cannot be empty")

    for task in tasks:
        if task["id"] == task_id:
            if payload.title is not None:
                task["title"] = payload.title.strip()
            if payload.done is not None:
                task["done"] = payload.done
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task", tags=["tasks"])
def delete_task(task_id: int):
    """Remove a task. Returns 204 with no body on success, 404 if unknown."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Extras — stats and reset (optional stretch)
# ---------------------------------------------------------------------------

@app.get("/stats", summary="Task stats", tags=["extras"])
def get_stats():
    """Return a small summary computed from the current task list."""
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    return {"total": total, "done": done_count, "open": total - done_count}


@app.post("/reset", summary="Reset to the 3 example tasks", tags=["extras"])
def reset_tasks():
    """Restore the in-memory list back to its original 3 example tasks."""
    seed_tasks()
    return {"status": "reset", "tasks": tasks}
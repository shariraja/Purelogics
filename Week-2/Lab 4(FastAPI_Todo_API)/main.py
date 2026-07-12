"""
Week 2 - Lab 4
FastAPI To-Do List REST API
----------------------------
Task: Develop a To-Do List REST API that allows users to
create, view, update, and delete tasks.

Endpoints:
1. POST   /todos          -> Add a new task
2. GET    /todos          -> Get all tasks
3. GET    /todos/{id}     -> Get a task by ID
4. PUT    /todos/{id}     -> Update a task
5. DELETE /todos/{id}     -> Delete a task
"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="To-Do List REST API")

# ---- Data Model ----
class Task(BaseModel):                         # Add new task(POST)
    title: str
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str
    completed: bool


# ---- Data Store (Database ki jagah Python list) ----
todos = []
next_id = 1


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}


# ---- Q1: Create a new task ----
@app.post("/todos")
def create_task(task: Task):
    global next_id
    new_task = {
        "id": next_id,
        "title": task.title,
        "completed": task.completed
    }
    todos.append(new_task)
    next_id += 1
    return new_task


# ---- Q2: Get all tasks ----
@app.get("/todos")
def get_all_tasks():
    return todos


# ---- Q3: Get a task by ID ----
@app.get("/todos/{task_id}")
def get_task(task_id: int):
    for task in todos:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# ---- Q4: Update a task ----
@app.put("/todos/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in todos:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# ---- Q5: Delete a task ----
@app.delete("/todos/{task_id}")
def delete_task(task_id: int):
    for task in todos:
        if task["id"] == task_id:
            todos.remove(task)
            return {"message": f"Task with id {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
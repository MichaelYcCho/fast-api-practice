import os
from pathlib import Path
from typing import List
from fastapi import Body, Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dotenv import load_dotenv


from database.connection import get_db

from database.orm import ToDo
from database.repository import get_todos
from schema.response import ListToDoResponse, ToDoSchema

current_file_path = Path(__file__).resolve()
BASE_DIR = current_file_path.parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"status": "ok"}


todo_data = {
    1: {"id": 1, "contents": "buy milk", "is_done": True},
    2: {"id": 2, "contents": "buy bread", "is_done": False},
    3: {"id": 3, "contents": "buy egg", "is_done": False},
}


@app.get("/todos", status_code=200)
def get_todos_handler(
    order: str | None = None, session: Session = Depends(get_db)
) -> ListToDoResponse:

    todos: List[ToDo] = get_todos(session)
    if order and order == "DESC":
        return ListToDoResponse(
            todos=[ToDoSchema.model_validate(todo) for todo in todos[::-1]]
        )
    return ListToDoResponse(todos=[ToDoSchema.model_validate(todo) for todo in todos])


@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int):
    todo = todo_data.get(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# DTO로 생각하면 될듯
class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool


@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateTodoRequest):
    todo_data[request.id] = request.model_dump()
    return todo_data[request.id]


# embed=True로 하면 body에 있는 값이 아래의 is_done에 들어간다.(하나의 필드만 뽑아서 사용할 때)
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(todo_id: int, is_done: bool = Body(..., embed=True)):
    todo = todo_data.get(todo_id, {})
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=200)
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="Todo not found")

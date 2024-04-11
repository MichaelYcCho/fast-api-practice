import os
from pathlib import Path
from typing import List
from fastapi import Body, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database.connection import get_db

from database.orm import ToDo
from database.repository import (
    create_todo,
    delete_todo,
    get_todo_by_todo_id,
    get_todos,
    update_todo,
)
from schema.request import CreateTodoRequest
from schema.response import ToDoResponseSchema, ToDoSchema


current_file_path = Path(__file__).resolve()
BASE_DIR = current_file_path.parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


todo_data = {
    1: {"id": 1, "contents": "buy milk", "is_done": True},
    2: {"id": 2, "contents": "buy bread", "is_done": False},
    3: {"id": 3, "contents": "buy egg", "is_done": False},
}


router = APIRouter(prefix="/todos")


@router.get("", status_code=200)
def get_todos_handler(
    order: str | None = None, session: Session = Depends(get_db)
) -> ToDoResponseSchema:

    todos: List[ToDo] = get_todos(session)
    if order and order == "DESC":
        return ToDoResponseSchema(
            todos=[ToDoSchema.model_validate(todo) for todo in todos[::-1]]
        )
    return ToDoResponseSchema(todos=[ToDoSchema.model_validate(todo) for todo in todos])


@router.get("/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int, session: Session = Depends(get_db)):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("", status_code=201)
def create_todo_handler(request: CreateTodoRequest, session: Session = Depends(get_db)):
    todo: ToDo = ToDo.create(request)  # id = None
    todo: ToDo = create_todo(session=session, todo=todo)  # id = int
    return ToDoSchema.model_validate(todo)


# embed=True로 하면 body에 있는 값이 아래의 is_done에 들어간다.(하나의 필드만 뽑아서 사용할 때)
@router.patch("/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        todo.done() if is_done else todo.undone
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    delete_todo(session=session, todo=todo)

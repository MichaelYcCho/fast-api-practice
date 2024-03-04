from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"status": "ok"}


todo_data = {
    1: {"id": 1, "contents": "buy milk", "is_done": True},
    2: {"id": 2, "contents": "buy bread", "is_done": False},
    3: {"id": 3, "contents": "buy egg", "is_done": False},
}


@app.get("/todos")
def get_todos_handler(order: str | None = None):
    ret = list(todo_data.values())

    if order == "desc":
        return ret[::-1]
    else:
        return ret


@app.get("/todos/{todo_id}")
def get_todo_handler(todo_id: int):
    return todo_data.get(todo_id, {})


# DTO로 생각하면 될듯
class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool


@app.post("/todos")
def create_todo_handler(request: CreateTodoRequest):
    todo_data[request.id] = request.model_dump()
    return todo_data[request.id]

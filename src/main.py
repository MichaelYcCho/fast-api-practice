from fastapi import Body, FastAPI, HTTPException
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

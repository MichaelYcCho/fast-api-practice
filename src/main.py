from fastapi import FastAPI

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

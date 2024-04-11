from fastapi import FastAPI
from api.todo import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def health_check_handler():
    return {"status": "ok"}

from pydantic import BaseModel


# DTO로 생각하면 될듯
class CreateTodoRequest(BaseModel):
    contents: str
    is_done: bool

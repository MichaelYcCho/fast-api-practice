from pydantic import BaseModel, ConfigDict


class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class ConfigDict:
        from_attributes = True


class ToDoResponseSchema(BaseModel):
    todos: list[ToDoSchema]
    # total_count: int
    # total_done: int
    # total_not_done: int

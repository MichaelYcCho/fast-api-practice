from typing import List

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from database.orm import ToDo


def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))


# scalar()는 있으면 값을 반환하고 없으면 None을 반환한다.
def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))


def create_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit()
    session.refresh(instance=todo)
    return todo


def update_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit()
    session.refresh(instance=todo)
    return todo


def delete_todo(session: Session, todo: ToDo) -> None:
    session.execute(delete(ToDo).where(ToDo.id == todo.id))
    session.commit()

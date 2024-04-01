from database.orm import ToDo


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_todos(client, mocker):

    mocker.patch(
        "main.get_todos",
        return_value=[
            {"id": 1, "contents": "buy milk", "is_done": True},
            {"id": 2, "contents": "buy bread", "is_done": True},
            {"id": 3, "contents": "buy egg", "is_done": True},
        ],
    )

    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "buy milk", "is_done": True},
            {"id": 2, "contents": "buy bread", "is_done": True},
            {"id": 3, "contents": "buy egg", "is_done": True},
        ]
    }

    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 3, "contents": "buy egg", "is_done": True},
            {"id": 2, "contents": "buy bread", "is_done": True},
            {"id": 1, "contents": "buy milk", "is_done": True},
        ]
    }


def test_get_todo(client, mocker):
    """
    # 200 test
    개별 테스트 : pytest src/tests/test_main.py::test_get_todo
    """

    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value={"id": 1, "contents": "buy milk", "is_done": True},
    )
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "buy milk", "is_done": True}


def test_get_todo_not_found(client, mocker):
    """
    # 404 test
    개별 테스트 : pytest src/tests/test_main.py::test_get_todo_not_found
    """

    mocker.patch("main.get_todo_by_todo_id", return_value=None)
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


# spy : 특정 객체를 트래킹할 수 있다
def test_create_todo(client, mocker):
    create_spy = mocker.spy(ToDo, "create")
    mocker.patch(
        "main.create_todo",
        return_value={"id": 1, "contents": "todo", "is_done": True},
    )

    body = {
        "contents": "test",
        "is_done": False,
    }
    response = client.post("/todos", json=body)
    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done == False

    assert create_spy.call_count == 1

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}


# def test_update_todo(client, mocker):
#     mocker.patch(
#         "main.get_todo_by_todo_id",
#         return_value=ToDo(id=1, contents="todo", is_done=True),
#     )
#     undone = mocker.patch.object(ToDo, "undone")
#     mocker.patch(
#         "main.update_todo",
#         return_value=ToDo(id=1, contents="todo", is_done=False),
#     )
#     response = client.patch("/todos/1", json={"is_done": False})
#     undone.assert_called_once_with()

#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "contents": "todo", "is_done": False}


def test_update_fail_todo(client, mocker):
    mocker.patch(
        "main.update_todo",
        return_value={"id": 1, "contents": "todo", "is_done": True},
    )

    response = client.patch("/todos/1", json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

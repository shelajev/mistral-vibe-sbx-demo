from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_lists_all_tasks_when_filter_is_absent() -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [1, 2, 3]


def test_filters_completed_tasks() -> None:
    response = client.get("/tasks", params={"completed": "true"})

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [1]


def test_filters_incomplete_tasks() -> None:
    response = client.get("/tasks", params={"completed": "false"})

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [2, 3]


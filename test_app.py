import os
import pytest
from app import app, DATA_FILE

@pytest.fixture
def client():
    app.config["TESTING"] = True
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    yield app.test_client()
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, To-Do App!" in response.data

def test_add_task(client):
    response = client.post("/tasks", json={"title": "Learn Docker"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Learn Docker"

def test_empty_title_rejected(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Learn Docker"})
    tasks = client.get("/tasks").get_json()
    assert len(tasks) == 1

def test_toggle_task(client):
    client.post("/tasks", json={"title": "Learn Docker"})
    client.put("/tasks/1")
    assert client.get("/tasks").get_json()[0]["done"] is True

def test_delete_task(client):
    client.post("/tasks", json={"title": "Learn Docker"})
    client.delete("/tasks/1")
    assert client.get("/tasks").get_json() == []
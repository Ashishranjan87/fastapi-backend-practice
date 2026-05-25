import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import status
from routers.Auth import get_current_user
from database import get_db
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user




def test_read_all(test_todos):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
      "title": "learn To Code!",
      "description": "Need to learn Everyday!",
      "priority": 5,
      "complete": False,
      "owner_id": 1
    }]


def test_read_one(test_todos):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
      "title": "learn To Code!",
      "description": "Need to learn Everyday!",
      "priority": 5,
      "complete": False,
      "owner_id": 1
    }


def test_create_todo(test_todos):
    request_data = {
        "title": "Make my Girlfriend Happy!",
        "description": "Need to take effort Everyday!",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }
    response = client.post("/todos/create_todos", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.complete == request_data["complete"]
    assert model.owner_id == request_data["owner_id"]


def test_update_todo(test_todos):
    request_data = {
      "title": "Updating learn To Code!",
      "description": "Need to learn Everyday!",
      "priority": 5,
      "complete": False,
      "owner_id": 1
    }
    response = client.put("/todos/update/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Updating learn To Code!"

def test_delete_todo(test_todos):
    response = client.delete("/todos/delete/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
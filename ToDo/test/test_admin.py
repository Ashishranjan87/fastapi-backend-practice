from datetime import datetime

from fastapi import status

from .utils import *
from database import get_db
from routers.Auth import get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_authenticated(test_todos):
    response = client.get("/admin/readAll")
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json() == [{
        "id": 1,
        "title": "learn To Code!",
        "description": "Need to learn Everyday!",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
        "created_at": None
    }]


def test_admin_delete_todo(test_todos):
    response = client.delete("/admin/delete/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
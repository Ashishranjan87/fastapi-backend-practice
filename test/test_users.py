from http.client import responses

from .utils import *
from fastapi import status
from database import get_db
from routers.Auth import get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()[0]

    assert data['username'] == "aashishr989"
    assert bcrypt_context.verify("Ranjan123", data['hashed_password'])
    assert data['email'] == "aashishr989"
    assert data['firstname'] == "Ashish"
    assert data['lastname'] == "Ranjan"
    assert data['role'] == "Admin"
    assert data['dateofbirth'] == "2000-05-21"
    assert data['phone_number'] == "9370038616"


def test_change_password(test_user):
    response = client.put("/user/password/", json={"password": "Ranjan123", "new_password": "Ashish123", "dateofbirth": "2000-05-21"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_updatePhoneNumber(test_user):
    response = client.put("/user/updatePhoneNumber/7633063440")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model.phone_number == "7633063440"
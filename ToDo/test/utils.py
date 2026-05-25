import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from database import Base
from main import app
from fastapi.testclient import TestClient
from routers.Auth import bcrypt_context
from models import Todos, Users


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


SQLALCHEMY_DATABASE_URI = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "aashishr989", "user_id": 1, "role": "Admin"}


@pytest.fixture()
def test_todos():
    todo = Todos(
        title = "learn To Code!",
        description = "Need to learn Everyday!",
        priority = 5,
        complete = False,
        owner_id = 1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()


@pytest.fixture()
def test_user():
    user = Users(
        username= "aashishr989",
        hashed_password= bcrypt_context.hash("Ranjan123"),
        email= "aashishr989",
        firstname= "Ashish",
        lastname= "Ranjan",
        role= "Admin",
        dateofbirth= date(2000, 5, 21),
        phone_number= "9370038616"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
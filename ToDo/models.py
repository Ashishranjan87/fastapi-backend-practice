from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date


class Secret(Base):
    __tablename__ = "secret"
    id = Column(Integer, primary_key=True)
    secret_key = Column(String)
    algorithm = Column(String)
    created_at = Column(Date)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    dateofbirth = Column(Date)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    created_at = Column(Date)
    phone_number = Column(String)


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date)

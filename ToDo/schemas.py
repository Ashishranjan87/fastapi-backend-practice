from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_validator


class CreateUser(BaseModel):
    username: str = Field(min_length=5, max_length=15)
    password: str = Field(min_length=8, max_length=72)
    email: EmailStr
    firstname: str = Field(min_length=1, max_length=15)
    lastname: str = Field(min_length=1, max_length=15)
    role: str = Field(min_length=1, max_length=5)
    dateofbirth: date|None = Field(default=None)
    phone_number: str = Field(min_length=1, max_length=10)

    @field_validator("dateofbirth")
    def validate_age(cls, dob: date):
        today = date.today()

        age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day)
        )

        if age < 18:
            raise ValueError("User must be at least 18 years old")

        return dob

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


class UserVerification(BaseModel):
    password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
    dateofbirth: date

class TodoResponse(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int
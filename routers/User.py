from fastapi import Depends, HTTPException, APIRouter, Path
from sqlalchemy.orm import Session
from typing import Annotated

from starlette import status

from database import get_db
from models import Users
from .Auth import get_current_user, bcrypt_context
from schemas import UserVerification

router = APIRouter(
    prefix="/user",
    tags=["user"]
)
db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependecy,db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(Users).filter(Users.id == user.get('user_id')).all()

@router.get("/getAllUser",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependecy,db: db_dependecy):
    if user is None or user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(Users).all()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependecy,
    db: db_dependecy,
    user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(
        Users.id == user.get('user_id')
    ).first()

    # Verify DOB
    if user_model.dateofbirth != user_verification.dateofbirth:
        raise HTTPException(
            status_code=401,
            detail="Date of birth does not match"
        )

    # Verify current password
    if not bcrypt_context.verify(
        user_verification.password,
        user_model.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail='Error on password change'
        )

    user_model.hashed_password = bcrypt_context.hash(
        user_verification.new_password
    )

    db.add(user_model)
    db.commit()


@router.put("/updatePhoneNumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(user: user_dependecy,db:db_dependecy,phone_number: str = Path(max_length=10)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    user_model.phone_number = phone_number
    try:
        db.add(user_model)
        db.commit()
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


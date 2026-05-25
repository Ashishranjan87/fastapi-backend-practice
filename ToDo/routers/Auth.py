from datetime import timedelta, timezone, datetime

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from database import get_db
from models import Users, Secret
from passlib.context import CryptContext
from jose import jwt, JWTError

from schemas import CreateUser

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

db_dependecy = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="Templates")

### Pages ###
@router.get("/login-page")
def login_page(request: Request):
    return templates.TemplateResponse(name="login.html", request=request)

@router.get("/register-page")
def register_page(request: Request):
    return templates.TemplateResponse(name="register.html", request=request)
### Endpoints ###

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_secret(db):
    return db.query(Secret).order_by(Secret.id.desc()).first()

def authenticate_user(username: str, password: str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(db,username: str, user_id: int, role: str, expires_delta: timedelta):
    payload = {'sub': username, 'id':user_id, 'role':role,'exp': datetime.now(timezone.utc) + expires_delta}
    secrets = get_secret(db)
    return jwt.encode(payload, secrets.secret_key, algorithm=secrets.algorithm)

async def get_current_user(db: db_dependecy,token: Annotated[str, Depends(Oauth2_bearer)]):
    secrets = get_secret(db)
    try:
        payload = jwt.decode(token, secrets.secret_key, algorithms=secrets.algorithm)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
        return {"username": username, "user_id": user_id, 'role':role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials", )



@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(db:db_dependecy, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(db, username=user.username, user_id=user.id,role=user.role, expires_delta=timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


@router.post("/createUser", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependecy, user_request: CreateUser):
    new_user = Users(email=user_request.email,
                        username=user_request.username,
                        dateofbirth=user_request.dateofbirth,
                        firstname=user_request.firstname,
                        lastname=user_request.lastname,
                        hashed_password=bcrypt_context.hash(user_request.password),
                        is_active=True,
                        role=user_request.role,
                        phone_number=user_request.phone_number
                        )
    try:
        db.add(new_user)
        db.commit()
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

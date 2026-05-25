from fastapi import Depends, HTTPException, Path, APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from typing import Annotated

from starlette import status

from database import get_db
from models import Todos
from .Auth import get_current_user



router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)
limiter = Limiter(key_func=get_remote_address)


db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]


@router.get("/readAll")
@limiter.limit("5/minute")
async def read_all(request: Request,user: user_dependecy,db: db_dependecy):
    if user is None or user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(Todos).all()


@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependecy,db: db_dependecy, todo_id: int=Path(gt=0)):
    if user is None or user.get('role') != "Admin":
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.delete(todo_model)
    db.commit()
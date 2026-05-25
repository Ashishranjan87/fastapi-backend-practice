from fastapi import Depends, HTTPException, Path, APIRouter, Request, status
from sqlalchemy.orm import Session
from typing import Annotated

from starlette.responses import RedirectResponse
from database import get_db
from models import Todos
from .Auth import get_current_user
from schemas import TodoRequest, TodoResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="Templates")
router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)
db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### Pages ###

@router.get("/todo-page")
async def render_todos(request: Request, db: db_dependecy):
    try:
        user = await get_current_user(db, request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()
        return templates.TemplateResponse(name="todo.html", request=request, context={"todos": todos, "user": user})
    except:
        return redirect_to_login()


@router.get("/add-todo-page")
async def render_add_todos(request: Request, db: db_dependecy):
    try:
        user = await get_current_user(db, request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse(name="add-todo.html", request=request, context={"user": user})
    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todos(request: Request, db: db_dependecy, todo_id: int):
    try:
        user = await get_current_user(db, request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        return templates.TemplateResponse(name="edit-todo.html", request=request, context={"todo": todo, "user": user})
    except Exception as error:
        print(error)
        return redirect_to_login()


### Endpoints ###


@router.get("/", response_model= list[TodoResponse])
async def read_all(user: user_dependecy,db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()

@router.get("/{todo_id}", status_code = status.HTTP_200_OK, response_model=TodoResponse)
async def get_todo(user: user_dependecy,db: db_dependecy, todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    todo_model = db.query(Todos).filter(Todos.id == todo_id,
                                        Todos.owner_id == user.get('user_id')).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found.")
    return todo_model

@router.post("/create_todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest,user: user_dependecy,db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = Todos(**todo_request.model_dump(), owner_id= user.get('user_id'))
    try:
        db.add(todo_model)
        db.commit()
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependecy,db: db_dependecy, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id,
                                        Todos.owner_id == user.get('user_id')).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found.")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()

@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependecy,db: db_dependecy, todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id,
                                        Todos.owner_id == user.get('user_id')).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.delete(todo_model)
    db.commit()
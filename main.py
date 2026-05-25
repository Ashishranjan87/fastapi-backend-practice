from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
import models
from database import engine
from routers import Auth, todos, admin, User

from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
def test(request: Request):
    return RedirectResponse("/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

app.include_router(Auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(User.router)
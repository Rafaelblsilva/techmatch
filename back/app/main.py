import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.database import get_db, initialize_beanie, start_db_client, stop_db_client
from app.core.exceptions import AppExceptionHandler
from app.middlewares.auth import UserDep
from app.routes import api_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setup the templates directory
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await start_db_client(app)
    db = get_db()
    await initialize_beanie(db)
    yield  
    # Shutdown
    await stop_db_client(app)


app = FastAPI(
    lifespan=lifespan
)

app.include_router(api_router)
AppExceptionHandler(app)


@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/healthcheck")
async def simple_message():
    return {"message": "OK"}


@app.get("/users/me")
async def read_users_me(current_user: UserDep):
    return current_user

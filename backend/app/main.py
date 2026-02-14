from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import models
from .database import engine

from .routers import users, auth , rooms, applications

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# models.Base.metadata.create_all(engine) [Alembic will do the job]

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(applications.router)


app.mount("/static", StaticFiles(directory="static")) # for static files ie. Images

@app.get('/')
def app_start():
    return {"Message":"Server Is Live"}
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import anime, info, user

models.Base.metadata.create_all(bind=engine)
# TODO pagination
# https://uriyyo-fastapi-pagination.netlify.app/first-steps/
app = FastAPI()

app.include_router(anime.router)
app.include_router(user.router)
app.include_router(info.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}

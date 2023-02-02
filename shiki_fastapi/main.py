from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
# TODO pagination
# https://uriyyo-fastapi-pagination.netlify.app/first-steps/
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/animes', response_model=list[schemas.Anime])
def get_anime_list(db: Session = Depends(get_db)):
    return crud.get_anime_list(db)


@app.get('/animes/{title}', response_model=schemas.Anime)
def get_anime(title: str, db: Session = Depends(get_db)):
    db_anime = crud.get_anime(db, title=title)
    if db_anime is None:
        raise HTTPException(status_code=404, detail='Anime not found')
    return db_anime


@app.get('/{username}', response_model=schemas.User)
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.get('/{username}/list/anime', response_model=list[schemas.Review])
def get_user_review_list(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user.reviews


@app.get('/users', response_model=list[schemas.User])
def get_user_list(db: Session = Depends(get_db)):
    return crud.get_user_list(db)


@app.post('/users/sign_up', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='This username has already been taken.')
    return crud.create_user(db=db, user=user)

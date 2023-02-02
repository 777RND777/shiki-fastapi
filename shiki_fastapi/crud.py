from sqlalchemy.orm import Session

from . import models, schemas


def get_anime_list(db: Session):
    return db.query(models.Anime).all()


def get_anime(db: Session, title: str):
    return db.query(models.Anime).filter(models.Anime.title == title).first()


def get_user_list(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.User(username=user.username, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

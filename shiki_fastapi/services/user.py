from sqlalchemy.orm import Session

from .. import models, schemas


def get_user_list(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.User(username=user.username, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

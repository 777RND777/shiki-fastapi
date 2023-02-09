from sqlalchemy.orm import Session

from .. import models, schemas, utils


def get_user_list(db: Session):
    return db.query(models.User).all()


def sign_up(db: Session, user: schemas.UserCreate):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

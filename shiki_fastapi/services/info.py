from sqlalchemy.orm import Session

from .. import models, schemas


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

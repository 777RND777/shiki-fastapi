from typing import Optional

from sqlalchemy.orm import Session

from .. import models


def get_user(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

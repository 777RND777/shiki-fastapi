from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..services import info as info_services

router = APIRouter(
    prefix="/{username}",
    tags=['Info']
)


@router.get('/', response_model=schemas.User)
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = info_services.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.get('/list/anime', response_model=list[schemas.Review])
def get_user_review_list(username: str, db: Session = Depends(get_db)):
    db_user = info_services.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user.reviews

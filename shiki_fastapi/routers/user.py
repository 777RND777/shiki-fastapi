from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..services import info as info_services
from ..services import user as user_services

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/', response_model=list[schemas.User])
def get_user_list(db: Session = Depends(get_db)):
    return user_services.get_user_list(db)


@router.post('/sign_up', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = info_services.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='This username has already been taken.')
    return user_services.create_user(db=db, user=user)

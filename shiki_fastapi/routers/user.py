from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2
from ..services import info as info_services
from ..services import user as user_services

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/', response_model=list[schemas.User])
def get_user_list(db: Session = Depends(database.get_db)):
    return user_services.get_user_list(db)


@router.post('/sign_in', response_model=schemas.Token)
def sign_in(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create a token
    # return token
    access_token = oauth2.create_access_token(data={"user_id": user.pk})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/sign_up', response_model=schemas.User)
def sign_up(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = info_services.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='This username has already been taken.')
    return user_services.sign_up(db=db, user=user)

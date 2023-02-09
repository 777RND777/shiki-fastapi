from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..services import anime as anime_services

router = APIRouter(
    prefix="/animes",
    tags=['Animes']
)


@router.get('/', response_model=list[schemas.Anime])
def get_anime_list(db: Session = Depends(get_db)):
    return anime_services.get_anime_list(db)


@router.get('/{title}', response_model=schemas.Anime)
def get_anime(title: str, db: Session = Depends(get_db)):
    db_anime = anime_services.get_anime(db, title=title)
    if db_anime is None:
        raise HTTPException(status_code=404, detail='Anime not found')
    return db_anime


@router.post('/{title}/review', response_model=schemas.Review)
def get_anime(title: str, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_anime = anime_services.get_anime(db, title=title)
    if db_anime is None:
        raise HTTPException(status_code=404, detail='Anime not found')
    db_review = anime_services.create_review(db, review, db_anime)
    anime_services.update_anime_score(db, db_review.score, db_anime)
    return db_review

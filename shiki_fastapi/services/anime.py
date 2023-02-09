from typing import Optional

from sqlalchemy.orm import Session

from .. import models, schemas


def get_anime_list(db: Session) -> list[models.Anime]:
    return db.query(models.Anime).all()


def get_anime(db: Session, title: str) -> Optional[models.Anime]:
    return db.query(models.Anime).filter(models.Anime.title == title).first()


def create_review(db: Session, review: schemas.ReviewCreate, anime: models.Anime, user_id: int) -> models.Review:
    db_review = db.query(models.Review).filter((models.Review.anime_id == anime.pk) &
                                               (models.Review.user_id == user_id)).first()
    if db_review:
        return update_review(db, db_review, review)

    if review.status == models.REVIEW_STATUS_CHOICE['COMPLETED']:
        review.watched_episodes = anime.episodes
    db_review = models.Review(anime_id=anime.pk, user_id=user_id,
                              status=review.status, watched_episodes=review.watched_episodes,
                              score=review.score, text=review.text)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(db: Session, db_review: models.Review, review: schemas.ReviewCreate) -> models.Review:
    if review.watched_episodes is None:
        db_review.watched_episodes = review.watched_episodes
    if review.status == models.REVIEW_STATUS_CHOICE['COMPLETED'] and db_review.status != review.status:
        review.watched_episodes = db_review.anime.episodes
    db_review.status = review.status
    db_review.score = review.score
    db_review.text = review.text

    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_anime_score(db: Session, score: int, anime: models.Anime) -> None:
    def get_anime_score(anime_id: int) -> float:
        reviews = db.query(models.Review).filter((models.Review.anime_id == anime_id) &
                                                 (models.Review.score > 0)).all()
        if len(reviews) == 0:
            return 0

        score_sum = 0
        for review in reviews:
            score_sum += review.score
        return round(score_sum / len(reviews), 2)

    if score == 0:
        return
    anime.score = get_anime_score(anime.pk)
    db.add(anime)
    db.commit()
    db.refresh(anime)

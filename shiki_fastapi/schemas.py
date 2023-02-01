from enum import Enum
from typing import Union

from pydantic import BaseModel


# class GenreBase(BaseModel):
#     name: str
#
#
# class GenreCreate(GenreBase):
#     pass
#
#
# class Genre(GenreBase):
#     pk: int
#     animes: list['Anime']
#
#     class Config:
#         orm_mode = True


class StudioBase(BaseModel):
    name: str


class StudioCreate(StudioBase):
    pass


class Studio(StudioBase):
    pk: int
    animes: list['Anime']

    class Config:
        orm_mode = True


class AnimeKindEnum(str, Enum):
    TV_SERIES = 'tv'
    MOVIE = 'movie'
    OVA = 'ova'
    ONA = 'ona'
    SPECIAL = 'special'
    MUSIC = 'music'


class AnimeStatusEnum(str, Enum):
    ANNOUNCED = 'anons'
    AIRING = 'ongoing'
    FINISHED = 'released'


class AnimeBase(BaseModel):
    title: str
    kind: 'AnimeKindEnum'
    episodes: int
    status: 'AnimeStatusEnum'
    # genres: list['Genre']
    synopsis: str

    class Config:
        use_enum_values = True


class AnimeCreate(AnimeBase):
    studio_id: int


class Anime(AnimeBase):
    pk: int
    score: float
    studio: str

    class Config:
        orm_mode = True


class ReviewStatusEnum(str, Enum):
    PLANNED_TO_WATCH = 'planned'
    WATCHING = 'watching'
    REWATCHING = 'rewatching'
    COMPLETED = 'completed'
    ON_HOLD = 'on_hold'
    DROPPED = 'dropped'


class ReviewBase(BaseModel):
    anime_id: int
    user_id: int
    status: 'ReviewStatusEnum'

    class Config:
        use_enum_values = True


class ReviewCreate(ReviewBase):
    watched_episodes: Union[int, None] = None
    score: Union[int, None] = None
    text: Union[str, None] = None


class Review(ReviewBase):
    pk: int
    watched_episodes: Union[int, None]
    score: Union[int, None]
    text: Union[str, None]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    pk: int
    reviews: list['Review']

    class Config:
        orm_mode = True

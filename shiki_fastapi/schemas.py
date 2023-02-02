from typing import Union

from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    pk: int

    class Config:
        orm_mode = True


class StudioBase(BaseModel):
    name: str


class StudioCreate(StudioBase):
    pass


class Studio(StudioBase):
    pk: int
    animes: list['Anime']

    class Config:
        orm_mode = True


class AnimeBase(BaseModel):
    title: str
    kind: str
    episodes: int
    status: str
    genres: list['GenreBase']
    synopsis: str


class AnimeCreate(AnimeBase):
    studio_id: int


class Anime(AnimeBase):
    pk: int
    score: float = None
    studio: 'StudioBase'

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    anime_id: int
    user_id: int
    status: str


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

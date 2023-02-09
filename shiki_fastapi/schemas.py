from typing import Union

from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    pk: int
    animes: list['Anime']


class StudioBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class StudioCreate(StudioBase):
    pass


class Studio(StudioBase):
    pk: int
    animes: list['Anime']


class AnimeBase(BaseModel):
    title: str
    kind: str
    episodes: int
    status: str
    genres: list['GenreBase']
    synopsis: str

    class Config:
        orm_mode = True


class AnimeCreate(AnimeBase):
    studio_id: int


class Anime(AnimeBase):
    pk: int
    score: float = None
    studio: 'StudioBase'


class ReviewBase(BaseModel):
    status: str


class ReviewCreate(ReviewBase):
    watched_episodes: Union[int, None] = None
    score: Union[int, None] = None
    text: Union[str, None] = None


class Review(ReviewBase):
    pk: int
    anime_id: int
    watched_episodes: Union[int, None]
    score: Union[int, None]
    text: Union[str, None]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    pk: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Union[str, None]

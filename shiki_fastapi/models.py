from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Genre(Base):
    __tablename__ = 'genres'

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    animes = relationship('Anime', back_populates='genres')

    def __str__(self):
        return self.name


class Studio(Base):
    __tablename__ = 'studios'

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    def __str__(self):
        return self.name


class Anime(Base):
    __tablename__ = 'animes'

    pk = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    kind = Column(String)  # choices
    episodes = Column(Integer)
    status = Column(String)  # choices
    genres = relationship('Genre', back_populates='animes')
    score = Column(Float)
    studio_id = Column(Integer, ForeignKey('studios.pk'))
    studio = relationship('Studio', back_populates='animes')
    synopsis = Column(Text)

    def __str__(self):
        return self.title


class Review(Base):
    __tablename__ = 'reviews'

    pk = Column(Integer, primary_key=True, index=True)
    anime_id = Column(Integer, ForeignKey('animes.pk'))
    anime = relationship('Anime', back_populates='reviews')
    user_id = Column(Integer, ForeignKey('users.pk'))
    user = relationship('User', back_populates='reviews')
    status = Column(String)  # choices
    watched_episodes = Column(Integer)
    score = Column(Integer)
    text = Column(Text)

    def __str__(self):
        return f'{self.score} for {self.anime} from {self.user}'


class User(Base):
    __tablename__ = 'users'

    pk = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

    def __str__(self):
        return self.username

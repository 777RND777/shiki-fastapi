import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .database import Base


association_table = Table(
    "association_table",
    Base.metadata,
    Column("anime_pk", ForeignKey("animes.pk")),
    Column("genre_pk", ForeignKey("genres.pk")),
)


class Genre(Base):
    __tablename__ = 'genres'

    pk = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    animes = relationship('Anime', secondary=association_table,
                          back_populates='genres', lazy=True)

    def __str__(self):
        return self.name


class Studio(Base):
    __tablename__ = 'studios'

    pk = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    animes = relationship('Anime', back_populates='studio', lazy=True)

    def __str__(self):
        return self.name


class Anime(Base):
    __tablename__ = 'animes'

    class Kind(enum.Enum):
        TV_SERIES = 'tv'
        MOVIE = 'movie'
        OVA = 'ova'
        ONA = 'ona'
        SPECIAL = 'special'
        MUSIC = 'music'

    class Status(enum.Enum):
        ANNOUNCED = 'anons'
        AIRING = 'ongoing'
        FINISHED = 'released'

    pk = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    kind = Column(Enum(Kind))
    episodes = Column(Integer)
    status = Column(Enum(Status))
    genres = relationship('Genre', secondary=association_table,
                          back_populates='animes', lazy=True)
    score = Column(Float)
    studio_id = Column(Integer, ForeignKey('studios.pk'))
    studio = relationship('Studio', back_populates='animes', lazy=True)
    synopsis = Column(Text)
    reviews = relationship('Review', back_populates='anime', lazy=True)

    def __str__(self):
        return self.title


class Review(Base):
    __tablename__ = 'reviews'

    class Status(enum.Enum):
        PLANNED_TO_WATCH = 'planned'
        WATCHING = 'watching'
        REWATCHING = 'rewatching'
        COMPLETED = 'completed'
        ON_HOLD = 'on_hold'
        DROPPED = 'dropped'

    pk = Column(Integer, primary_key=True)
    anime_id = Column(Integer, ForeignKey('animes.pk'))
    anime = relationship('Anime', back_populates='reviews', lazy=True)
    user_id = Column(Integer, ForeignKey('users.pk'))
    user = relationship('User', back_populates='reviews', lazy=True)
    status = Column(Enum(Status))
    watched_episodes = Column(Integer)
    score = Column(Integer)
    text = Column(Text)

    def __str__(self):
        return f'{self.score} for {self.anime} from {self.user}'


class User(Base):
    __tablename__ = 'users'

    pk = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    reviews = relationship('Review', back_populates='user', lazy=True)

    def __str__(self):
        return self.username

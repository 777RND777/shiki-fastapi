from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Text, types
from sqlalchemy.orm import relationship

from .database import Base

association_table = Table(
    'association_table',
    Base.metadata,
    Column('anime_pk', ForeignKey('animes.pk')),
    Column('genre_pk', ForeignKey('genres.pk')),
)


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kwargs):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


ANIME_KIND_CHOICE = {
    'TV_SERIES': 'tv',
    'MOVIE': 'movie',
    'OVA': 'ova',
    'ONA': 'ona',
    'SPECIAL': 'special',
    'MUSIC': 'music'
}
ANIME_STATUS_CHOICE = {
    'ANNOUNCED': 'anons',
    'AIRING': 'ongoing',
    'FINISHED': 'released'
}
REVIEW_STATUS_CHOICE = {
    'PLANNED_TO_WATCH': 'planned',
    'WATCHING': 'watching',
    'REWATCHING': 'rewatching',
    'COMPLETED': 'completed',
    'ON_HOLD': 'on_hold',
    'DROPPED': 'dropped'
}


class Genre(Base):
    __tablename__ = 'genres'

    pk = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    animes = relationship('Anime', secondary=association_table,
                          back_populates='genres', lazy=True)

    def __str__(self):
        return self.name


class Studio(Base):
    __tablename__ = 'studios'

    pk = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    animes = relationship('Anime', back_populates='studio', lazy=True)

    def __str__(self):
        return self.name


class Anime(Base):
    __tablename__ = 'animes'

    pk = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    kind = Column(ChoiceType(ANIME_KIND_CHOICE), nullable=False)
    episodes = Column(Integer, nullable=False)
    status = Column(ChoiceType(ANIME_STATUS_CHOICE), nullable=False)
    genres = relationship('Genre', secondary=association_table,
                          back_populates='animes', lazy=True)
    score = Column(Float)
    studio_id = Column(Integer, ForeignKey('studios.pk'), nullable=False)
    studio = relationship('Studio', back_populates='animes', lazy=True)
    synopsis = Column(Text, nullable=False)
    reviews = relationship('Review', back_populates='anime', lazy=True)

    def __str__(self):
        return self.title


class Review(Base):
    __tablename__ = 'reviews'

    pk = Column(Integer, primary_key=True)
    anime_id = Column(Integer, ForeignKey('animes.pk'), nullable=False)
    anime = relationship('Anime', back_populates='reviews', lazy=True)
    user_id = Column(Integer, ForeignKey('users.pk'), nullable=False)
    user = relationship('User', back_populates='reviews', lazy=True)
    status = Column(ChoiceType(REVIEW_STATUS_CHOICE), nullable=False)
    watched_episodes = Column(Integer)
    score = Column(Integer)
    text = Column(Text)

    def __str__(self):
        return f'{self.score} for {self.anime} from {self.user}'


class User(Base):
    __tablename__ = 'users'

    pk = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    reviews = relationship('Review', back_populates='user', lazy=True)

    def __str__(self):
        return self.username

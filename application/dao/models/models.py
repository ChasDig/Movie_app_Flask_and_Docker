import json

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from application.setup.db import models, db


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


#
class Director(models.Base):
    __tablename__ = "director"

    name = Column(String(100), unique=True, nullable=False)


#
favorites_movies = db.Table(
    "favorites",
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column("movies_id", db.Integer, db.ForeignKey('movie.id'), primary_key=True)
)


#
class Movie(models.Base):
    __tablename__ = "movie"

    title = Column(String(100))
    description = Column(String(255))
    trailer = Column(String(100))
    year = Column(Integer)
    rating = Column(Float)

    genre_id = Column(Integer, ForeignKey(f"{Genre.__tablename__}.id"), nullable=False)
    genre = relationship("Genre")

    director_id = Column(Integer, ForeignKey(f"{Director.__tablename__}.id"), nullable=False)
    director = relationship("Director")


#
class User(models.Base):
    __tablename__ = "user"

    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favorite_genre = Column(Integer, ForeignKey(f"{Genre.__tablename__}.id"))
    favorites = db.relationship(
        'Movie',
        secondary=favorites_movies,
        lazy="subquery",
        backref=db.backref('movie', lazy=True),
    )




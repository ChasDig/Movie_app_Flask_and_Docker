import json

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from application.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


#
class Director(models.Base):
    __tablename__ = "director"

    name = Column(String(100), unique=True, nullable=False)


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


class FavoritesMovies(models.Base):
    __tablename__ = "favorites_movies"

    user_id = Column(Integer, ForeignKey(f"{User.__tablename__}.id)"))
    movie_id = Column(Integer, ForeignKey(f"{Movie.__tablename__}.id"))

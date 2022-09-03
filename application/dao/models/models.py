from sqlalchemy import Column, String, Integer, Float, ForeignKey
from marshmallow import Schema, fields
from sqlalchemy.orm import relationship

from application.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


#
class Director(models.Base):
    __tablename__ = "director"

    name = Column(String(100), uniqule=True, nullable=False)


#
class Movie(models.Base):
    __tablename__ = "movie"

    title = Column(String(100))
    description = Column(String(255))
    trailer = Column(String(100))
    year = Column(Integer)
    rating = Column(Float)

    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=False)
    genre = relationship("Genre")

    director_id = Column(Integer, ForeignKey="director.id", nullable=False)
    director = relationship("Director")


#
class User(models.Base):
    __tablename__ = "user"

    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favorite_genre = Column(String())
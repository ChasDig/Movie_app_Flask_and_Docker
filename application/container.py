from application.dao import GenresDAO, DirectorsDAO, MoviesDAO, UsersDAO, FavoritesMoviesDAO

from application.services import GenresService, DirectorsService, MoviesService, UsersService, FavoritesMoviesService
from application.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorsDAO(db.session)
movie_dao = MoviesDAO(db.session)
user_dao = UsersDAO(db.session)
favorites_movies_dao = FavoritesMoviesDAO(db.session)


# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UsersService(dao=user_dao)
favorites_movies_service = FavoritesMoviesService(dao=favorites_movies_dao)

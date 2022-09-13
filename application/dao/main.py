from typing import Optional, List

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from application.dao.base import BaseDAO, T
from application.dao.models.models import Genre
from application.dao.models.models import Director
from application.dao.models.models import Movie
from application.dao.models.models import User, favorites_movies


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all(self, page: Optional[int] = None, filter: Optional[str] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)

        if filter != "new":
            stmt = stmt.order_by(desc(self.__model__.year))

        else:
            stmt = stmt.order_by(self.__model__.year)

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    #
    def get_by_email(self, email: str):
        stmt: BaseQuery = self._db_session.query(self.__model__).filter(self.__model__.email == email).one()
        return stmt

    #
    def create_user(self, email: str, password: str):
        new_user = User(email=email, password=password)
        self._db_session.add(new_user)
        self._db_session.commit()
        return new_user

    def update_data_user(self, data_json, email):
        user_update = self._db_session.query(self.__model__).filter(self.__model__.email == email).update(data_json)
        self._db_session.commit()
        return user_update

    def update_password_user(self, new_password, email):
        # user_update = self._db_session.query(self.__model__).filter(self.__model__.email == email).update(password=new_password)
        user_update = self.get_by_email(email)
        user_update.password = new_password
        self._db_session.add(user_update)
        self._db_session.commit()

        return user_update

    #
    def add_favorite_movies(self, user_id: str, movie_id: str):
        favorites_movies_new = favorites_movies.insert().values(user_id=user_id, movies_id=movie_id)
        self._db_session.execute(favorites_movies_new)
        self._db_session.commit()
        return favorites_movies_new

    #
    def delete_favorite_movies(self, movie_id: str):
        self._db_session.query(favorites_movies).filter(favorites_movies.c.movies_id == movie_id).delete()
        self._db_session.commit()
        return 'Favorite movie delete!'

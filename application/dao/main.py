import json
from typing import Optional, List

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from application.dao.base import BaseDAO, T
from application.dao.models.models import Genre
from application.dao.models.models import Director
from application.dao.models.models import Movie
from application.dao.models.models import User
from application.dao.models.models import FavoritesMovies


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
        return 'User create!'

    def update_data_user(self, data_json, email):
        self._db_session.query(self.__model__).filter(self.__model__.email == email).update(data_json)
        self._db_session.commit()
        return "User update!"

    def update_password_user(self, new_password, email):
        user = self.get_by_email(email)
        user.password = new_password
        self._db_session.add(user)
        self._db_session.commit()

        return user


class FavoritesMoviesDAO(BaseDAO[FavoritesMovies]):
    __model__ = FavoritesMovies

    def get_by_email(self, email: str):
        stmt: BaseQuery = self._db_session.query(User).filter(User.email == email).first()
        return json.dumps(stmt)

    def add_movie_favorite(self, movie_id, email):
        data = self.get_by_email(email=email)
        return data

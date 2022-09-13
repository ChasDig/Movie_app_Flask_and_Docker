import pytest

from application.dao.models.models import Movie
from application.dao import MoviesDAO


class TestMovieDAO:

    @pytest.fixture()
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture()
    def movie_1(self, db):
        m = Movie(title="test_title_1", description="test_description_1", trailer="test_trailer_1", year=1, rating=1.1,
                  genre_id=1, director_id=1)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture()
    def movie_2(self, db):
        m = Movie(title="test_title_2", description="test_description_2", trailer="test_trailer_2", year=2, rating=2.2,
                  genre_id=2, director_id=2)
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movies_dao, movie_1):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all(filter="new") == [movie_1, movie_2]

    def test_get_all_movies_filter_is_none(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all(filter=None) == [movie_2, movie_1]

    def test_get_movies_by_page(self, movies_dao, movie_1, movie_2, app):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1, filter="new") == [movie_1]
        assert movies_dao.get_all(page=2, filter="new") == [movie_2]
        assert movies_dao.get_all(page=3, filter="new") == []

    def test_get_movies_by_page_filter_is_none(self, movies_dao, movie_1, movie_2, app):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1, filter=None) == [movie_2]
        assert movies_dao.get_all(page=2, filter=None) == [movie_1]
        assert movies_dao.get_all(page=3, filter=None) == []

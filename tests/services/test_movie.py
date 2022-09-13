import pytest
from unittest.mock import patch

from application.dao.models.models import Movie
from application.services import MoviesService
from application.exceptions import ItemNotFound


class TestUserService:

    @pytest.fixture()
    @patch('application.dao.MoviesDAO')
    def movies_dao_mock(self, movies_mock):
        dao = movies_mock()
        dao.get_by_id.return_value = Movie(id=1, title="test_title_1", description="test_description_1",
                                           trailer="test_trailer_1", year=1, rating=1.1, genre_id=1, director_id=1)
        dao.get_all.return_values = [
            Movie(id=1, title="test_title_1", description="test_description_1",
                  trailer="test_trailer_1", year=1, rating=1.1, genre_id=1, director_id=1),
            Movie(id=2, title="test_title_2", description="test_description_2",
                  trailer="test_trailer_2", year=2, rating=2.2, genre_id=2, director_id=2)
        ]

        return dao

    @pytest.fixture()
    def movies_service(self, movies_dao_mock):
        return MoviesService(dao=movies_dao_mock)

    @pytest.fixture()
    def movie_1(self, db):
        m = Movie(id=1, title="title_1", description="description_1",
                  trailer="trailer_1", year=10, rating=1.0, genre_id=10, director_id=10)
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie(self, movies_service, movie_1):
        assert movies_service.get_item(movie_1.id)

    def test_get_movie_not_found(self, movies_service, movies_dao_mock):
        movies_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            movies_service.get_item(12)

    # @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    # def test_get_movies(self, movies_dao_mock, movies_service, page):
    #     movies = movies_service.get_all(page=page)
    #     assert len(movies) == 2
    #     assert movies == movies_dao_mock.get_all.return_value
    #     movies_dao_mock.get_all.assert_called_with(page=page)

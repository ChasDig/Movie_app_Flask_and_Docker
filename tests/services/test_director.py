import pytest
from unittest.mock import patch

from application.exceptions import ItemNotFound
from application.dao.models.models import Director
from application.services import DirectorsService


class TestDirectorService:

    @pytest.fixture()
    @patch('application.dao.DirectorsDAO')
    def director_dao_mock(self, dao_mock):
        dao = dao_mock
        dao.get_by_id.return_value = Director(id=1, name="test_director")
        dao.get_all.return_value = [
            Director(id=1, name='test_director_1'),
            Director(id=2, name='test_director_2')
        ]
        return dao

    @pytest.fixture()
    def director_service(self, director_dao_mock):
        return DirectorsService(dao=director_dao_mock)

    @pytest.fixture()
    def director_1(self, db):
        d = Director(name='test_name_director')
        db.session.add(d)
        db.session.commit()

        return d

    def test_get_item(self, director_service, director_1):
        assert director_service.get_item(director_1.id)

    def test_director_found(self, director_service, director_dao_mock):
        director_dao_mock.get_by_id().return_value = None

        if pytest.raises(ItemNotFound):
            director_service.get_item(10)

    @pytest.mark.parametrize("page", [1, None], ids=["with_page", "without_page"])
    def test_get_directors(self, page, director_dao_mock, director_service):
        directors = director_service.get_all(page=page)
        assert len(directors) == 2
        assert directors == director_dao_mock.get_all.return_value
        director_dao_mock.get_all.assert_called_with(page=page)

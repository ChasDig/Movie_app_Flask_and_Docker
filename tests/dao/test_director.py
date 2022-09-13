import pytest

from application.dao.models.models import Director
from application.dao import DirectorsDAO

class TestDirectorDAO:

    @pytest.fixture()
    def director_dao(self, db):
        return DirectorsDAO(db.session)

    @pytest.fixture()
    def director_1(self, db):
        d = Director(name='test_director_1')
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture()
    def director_2(self, db):
        d = Director(name='test_director_2')
        db.session.add(d)
        db.session.commit()

        return d

    def test_get_director_by_id(self, director_1, director_dao):
        assert director_dao.get_by_id(director_1.id) == director_1

    def test_get_director_by_id_not_found(self, director_dao):
        assert not director_dao.get_by_id(1)

    def test_get_all_directors(self, director_1, director_2, director_dao):
        assert director_dao.get_all() == [director_1, director_2]

    def test_get_directors_by_page(self, app, director_1, director_2, director_dao):
        app.config['ITEMS_PER_PAGE'] = 1
        assert director_dao.get_all(page=1) == [director_1]
        assert director_dao.get_all(page=2) == [director_2]
        assert director_dao.get_all(page=3) == []

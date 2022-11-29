import pytest

from application.dao.models.models import Director


class TestDirectorViews:

    @pytest.fixture()
    def director(self, db):
        d = Director(name="director_test_1")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_many(self, client, director):
        response = client.get("/directors/")
        assert response.status_code == 200
        assert response.json == [{"id": director.id, "name": director.name}]

    def test_director_page(self, client, director):
        response = client.get("/directors/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/directors/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_director(self, client, director):
        response = client.get("/directors/?page=1")
        assert response.status_code == 200
        assert response.json == [{"id": director.id, "name": director.name}]

    def test_director_not_found(self, client, director):
        response = client.get("directors/=2")
        assert response.status_code == 404

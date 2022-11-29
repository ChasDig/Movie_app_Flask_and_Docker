import pytest

from application.dao import UsersDAO
from application.dao.models.models import User, favorites_movies


class TestUserDAO:

    @pytest.fixture
    def user_dao(self, db):
        return UsersDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        u = User(id=1, email="email_test_1@mail.ru", password="password_test_1", name="name_test_1", surname="surname_test_1",
                 favorite_genre=1)
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def user_2(self, db):
        u = User(id=2, email="email_test_2@mail.ru", password="password_test_2", name="name_test_2", surname="surname_test_2",
                 favorite_genre=2)
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def favorites_movies_1(self, db):
        f_m = favorites_movies.insert().values(user_id="1", movie_id="1")
        db.session.add(f_m)
        db.session.commit()
        return f_m

    def test_get_user_by_id(self, user_1, user_dao):
        assert user_dao.get_by_id(user_1.id) == user_1

    def test_get_user_by_id_not_found(self, user_dao):
        assert not user_dao.get_by_id(1)

    def test_get_all_users(self, user_dao, user_1, user_2):
        assert user_dao.get_all() == [user_1, user_2]

    def test_get_user_by_email(self, user_1, user_dao):
        assert user_dao.get_by_email(user_1.email) == user_1

    def test_create_user(self, user_1, user_dao):
        new_user = {
            "email": "email_test_new@mail.ru",
            "password": "password_new"
        }

        new_user_create = user_dao.create_user(email=new_user.get("email"), password=new_user.get("password"))

        assert new_user_create is not None
        assert new_user_create.email is not None
        assert new_user_create.password is not None
        assert new_user_create.email == new_user.get("email")
        assert new_user_create.password == new_user.get("password")

    def test_update_data_user(self, user_1, user_dao):
        user_for_update = {
            "id": 1,
            "email": "email_test_new@mail.ru",
            "name": "name_new",
            "surname": "surname_new",
            "favorite_genre": 3,
            "password": "password_new"
        }

        update_user = user_dao.update_data_user(email=user_1.email, data_json=user_for_update)
        user = user_dao.get_by_id(update_user)

        assert update_user is not None
        assert user is not None
        assert user.id == user_for_update.get("id")
        assert user.email == user_for_update.get("email")
        assert user.name == user_for_update.get("name")
        assert user.surname == user_for_update.get("surname")
        assert user.favorite_genre == user_for_update.get("favorite_genre")
        assert user.password == user_for_update.get("password")

    def test_password_user(self, user_1, user_dao):
        user_for_update = {
            "id": 1,
            "email": "email_test_new@mail.ru",
            "name": "name_new",
            "surname": "surname_new",
            "favorite_genre": 3,
            "password": "password_new_update"
        }

        update_password_user = user_dao.update_password_user(new_password=user_for_update.get("password"),
                                                             email=user_1.email)

        user = user_dao.get_by_id(update_password_user.id)

        assert update_password_user is not None
        assert user is not None
        assert user.id == user_1.id
        assert user.email == user_1.email
        assert user.name == user_1.name
        assert user.surname == user_1.surname
        assert user.favorite_genre == user_1.favorite_genre
        assert user.password == user_1.password


    def test_get_genres_by_page(self, app, user_dao, user_1, user_2):
        app.config['ITEMS_PER_PAGE'] = 1

        assert user_dao.get_all(page=1) == [user_1]
        assert user_dao.get_all(page=2) == [user_2]
        assert user_dao.get_all(page=3) == []

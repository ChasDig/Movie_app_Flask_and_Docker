from unittest.mock import patch

import pytest

from application.exceptions import ItemNotFound
from application.dao.models.models import User
from application.services import UsersService


class TestUsersService:

    @pytest.fixture()
    @patch('application.dao.UsersDAO')
    def users_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_id.return_value = User(id=5, email="email_test_5@mail.ru", password="password_test_5",
                                          name="name_test_5", surname="surname_test_5", favorite_genre=5)
        dao.get_all.return_value = [
            User(id=6, email="email_test_6@mail.ru", password="password_test_6",
                 name="name_test_6", surname="surname_test_6", favorite_genre=6),
            User(id=3, email="email_test_3@mail.ru", password="password_test_3", name="name_test_3",
                 surname="surname_test_3", favorite_genre=3),
        ]
        return dao

    @pytest.fixture()
    def users_service(self, users_dao_mock):
        return UsersService(dao=users_dao_mock)

    @pytest.fixture
    def user(self, db):
        obj = User(id=4, email="email_test_4@mail.ru", password="password_test_4", name="name_test_4",
                   surname="surname_test_4", favorite_genre=4)
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_user(self, users_service, user):
        assert users_service.get_by_email(user.email)

    def test_get_user_by_email(self, users_service, user):
        assert users_service.get_item(user.id)

    def test_create_user(self, users_service, user):

        data_user = {
            "email": "email_test_create@mail.ru",
            "password": "password_test_create"
        }

        create_user = users_service.create_user(email=data_user.get("email"), password=data_user.get("password"))
        assert create_user is not None

    def test_user_not_found(self, users_dao_mock, users_service):
        users_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            users_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_users(self, users_dao_mock, users_service, page):
        users = users_service.get_all(page=page)
        assert len(users) == 2
        assert users == users_dao_mock.get_all.return_value
        users_dao_mock.get_all.assert_called_with(page=page)

from typing import Optional

from application.dao.main import UsersDAO
from application.exceptions import ItemNotFound
from application.dao.models.models import User
from application.tools.security import generate_password_hash
from application.tools.security import get_data_by_token


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def get_by_email(self, email: str) -> User:
        return self.dao.get_by_email(email=email)

    def get_by_token(self, token: str) -> User:
        data = get_data_by_token(token)
        return self.dao.get_by_email(email=data.get("email"))

    def create_user(self, email: str, password: str) -> User:
        password = generate_password_hash(password)
        return self.dao.create_user(email=email, password=password)

    def update_data_user(self, data_json, token):
        email = get_data_by_token(token)
        return self.dao.update_data_user(data_json, email=email.get("email"))

    def update_password_user(self, data_json, token):
        email = get_data_by_token(token).get("email")
        new_password = generate_password_hash(password=data_json["new_password"])
        return self.dao.update_password_user(new_password=new_password, email=email)

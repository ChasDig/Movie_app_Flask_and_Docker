from application.dao.base import BaseDAO
from application.dao.models.models import Genre


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre

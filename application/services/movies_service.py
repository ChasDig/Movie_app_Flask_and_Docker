from typing import Optional

from application.dao.main import MoviesDAO
from application.exceptions import ItemNotFound
from application.dao.models.models import Movie


class MoviesService:
    def __init__(self, dao: MoviesDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Movie with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None, filter: Optional[str] = None) -> list[Movie]:
        return self.dao.get_all(page=page, filter=filter)


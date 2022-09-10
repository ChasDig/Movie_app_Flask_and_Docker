from application.dao.main import FavoritesMoviesDAO
from application.dao.models.models import FavoritesMovies
from application.tools.security import get_data_by_token


class FavoritesMoviesService:

    def __init__(self, dao: FavoritesMoviesDAO) -> None:
        self.dao = dao

    def add_movie_favorite(self, movie_id, token):
        data = get_data_by_token(token)
        return self.dao.add_movie_favorite(email=data.get("email"), movie_id=movie_id)

from application.dao import GenresDAO

from application.services import GenresService
from application.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)

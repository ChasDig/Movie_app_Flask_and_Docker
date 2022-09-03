from application.config import config
from application.dao.models.models import Genre
from application.server import create_app, db

app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
    }

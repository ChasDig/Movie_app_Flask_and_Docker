from application.config import config
from application.server import create_app
from application.setup.db import db

if __name__ == '__main__':
    with create_app(config).app_context():
        db.create_all()

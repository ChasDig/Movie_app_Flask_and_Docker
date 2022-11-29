from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from application.exceptions import BaseServiceError
from application.setup.api import api
from application.setup.db import db
from application.views import auth_ns, genres_ns, user_ns, directors_ns, movies_ns, favorites_movies_ns


def base_service_error_handler(exception: BaseServiceError):
    return jsonify({'error': str(exception)}), exception.code


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    migrate = Migrate(app, db)

    CORS(app=app)
    db.init_app(app)
    api.init_app(app)

    # Регистрация эндпоинтов:
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(favorites_movies_ns)

    app.register_error_handler(BaseServiceError, base_service_error_handler)

    return app

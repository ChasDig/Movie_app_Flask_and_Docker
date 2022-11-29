from flask_restx import fields, Model

from application.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})


#
director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Квентин Тарантино'),
})

#
movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example="Текст"),
    'description': fields.String(required=True, max_length=100, example="Текст"),
    'trailer': fields.String(required=True, max_length=100, example="Текст"),
    'year': fields.Integer(required=True, example=1),
    'rating': fields.Float(required=True, example=1),
    'genre_id': fields.Integer(required=True, example=1),
    'director_id': fields.Integer(required=True, example=1),
})

favorites: Model = api.model("Любимые фильмы", {
    'user_id': fields.Integer(required=True, example=1),
    'movie_id': fields.Integer(required=True, example=1)
})

#
user: Model = api.model("Пользователь", {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=50, example="Текст"),
    'password': fields.String(required=True, max_length=50, example="Текст"),
    'name': fields.String(required=True, max_length=100, example="Текст"),
    'surname': fields.String(required=True, max_length=100, example="Текст"),
    'favorite_genre': fields.Nested(genre),
    "favorites": fields.Nested(favorites),
})



from flask_restx import Namespace, Resource
from flask import request, abort

from application.setup.api.models import user
from application.setup.api.parsers import page_parser

from application.container import user_service

api = Namespace('favorites')


#
@api.route('/movies/<int:movie_id>')
class FavoritesViews(Resource):

    @api.expect(page_parser)
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self, movie_id):

        token = request.headers['Authorization'].split('Bearer ')[-1]

        if not token:
            print("Token not found!")
            abort(401)
        user = user_service.get_by_token(token)

        return user_service.add_favorite_movies(user_id=user.id, movie_id=movie_id)

    @api.expect(page_parser)
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def delete(self, movie_id):

        return user_service.delete_favorite_movies(movie_id=movie_id)

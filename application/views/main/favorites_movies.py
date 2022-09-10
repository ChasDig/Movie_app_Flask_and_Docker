from flask_restx import Namespace, Resource
from flask import request, abort

from application.container import favorites_movies_service
from application.setup.api.models import favorites_movies
from application.setup.api.parsers import page_parser

api = Namespace('favorites')


#
@api.route('/movies/<int:movie_id>')
class FavoritesViews(Resource):

    @api.expect(page_parser)
    @api.marshal_with(favorites_movies, as_list=True, code=200, description='OK')
    def post(self, movie_id):

        token = request.headers['Authorization'].split('Bearer ')[-1]

        if not token:
            print("Token not found!")
            abort(401)
        return favorites_movies_service.add_movie_favorite(movie_id=movie_id, token=token)


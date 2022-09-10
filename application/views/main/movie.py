from flask_restx import Namespace, Resource
from flask import request

from application.container import movie_service
from application.setup.api.models import movie
from application.setup.api.parsers import page_parser
from application.tools.decorators import auth_required

api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):

    @api.expect(page_parser)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all movies.
        """
        status = request.args.get("status")
        return movie_service.get_all(filter=status, **page_parser.parse_args())


@api.route('/<int:movie_id>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, movie_id: int):
        """
        Get movie by id.
        """
        return movie_service.get_item(movie_id)

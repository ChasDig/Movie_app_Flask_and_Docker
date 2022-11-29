from flask_restx import Namespace, Resource
from flask import request, abort

from application.container import user_service
from application.setup.api.models import user
from application.setup.api.parsers import page_parser
from application.tools.decorators import auth_required

api = Namespace('users')


@api.route('/')
class UsersView(Resource):

    @auth_required
    @api.expect(page_parser)
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        token = request.headers['Authorization'].split("Bearer ")[-1]
        if token:
            return user_service.get_by_token(token=token)

    @auth_required
    @api.expect(page_parser)
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def patch(self):

        data_json = request.json

        token = request.headers['Authorization'].split("Bearer ")[-1]

        if not data_json['name'] or not data_json['surname'] or not data_json['favorite_genre']:
            print("Not found name, surname or favorite_genre!")
            abort(401)

        return user_service.update_data_user(data_json=data_json, token=token)


@api.route('/password/')
class UsersPasswordView(Resource):

    @auth_required
    @api.expect(page_parser)
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def put(self):

        data_json = request.json

        token = request.headers['Authorization'].split("Bearer ")[-1]

        if not data_json['new_password']:
            print("Not found old_password or new_password!")
            abort(401)

        return user_service.update_password_user(data_json=data_json, token=token)

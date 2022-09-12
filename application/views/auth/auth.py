from flask_restx import Namespace, Resource
from flask import request, abort

from application.setup.api.models import user
from application.tools.security import generate_token, confirm_refresh_token
from application.container import user_service

api = Namespace('auth')


@api.route('/register/')
class AuthViewsRegister(Resource):

    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        data_json = request.json
        if not data_json.get('email') or not data_json.get('password'):
            print("User is not found!")
            abort(401)

        return user_service.create_user(email=data_json.get("email"), password=data_json.get("password"))


@api.route('/login/')
class AuthViewsLogin(Resource):

    def post(self):
        data_json = request.json
        print(data_json['password'])
        if not data_json.get('email') or not data_json.get('password'):
            print("User is not found!")
            abort(401)

        return generate_token(email=data_json['email'], password=data_json['password'],
                              password_hash=user_service.get_by_email(data_json['email']).password, is_refresh=False)

    def put(self):

        json_data = request.json
        print(json_data.get("refresh_token"))

        if not json_data.get("refresh_token"):
            print("Refresh token not found!")
            abort(401)
        return confirm_refresh_token(json_data.get("refresh_token"))


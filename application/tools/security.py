import base64
import hashlib
import datetime
import calendar
import jwt

from flask import current_app, abort


def generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(generate_password_digest(password)).decode('utf-8')


#
def compare_password_and_hash(password, password_hash):
    return password_hash == generate_password_hash(password=password)


#
def generate_token(email, password, password_hash, is_refresh=False):

    if not is_refresh:
        if not compare_password_and_hash(password=password, password_hash=password_hash):
            return "Error!"

    data = {
        'email': email,
        'password': password
    }

    min_token = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
    data['exp'] = calendar.timegm(min_token.timetuple())
    access_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGORITHM"])

    day_token = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config["TOKEN_EXPIRE_DAYS"])
    data['exp'] = calendar.timegm(day_token.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGORITHM"])

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def confirm_refresh_token(refresh_token: str):
    data = jwt.decode(refresh_token, key=current_app.config["SECRET_KEY"], algorithms=current_app.config["ALGORITHM"])

    email = data.get('email')
    password = data.get('password')

    return generate_token(email=email, password=password, password_hash=None, is_refresh=True)


def get_data_by_token(token: str):

    data = jwt.decode(token, key=current_app.config["SECRET_KEY"], algorithms=current_app.config["ALGORITHM"])
    return data

import jwt
import json
import datetime
import os
from flask import Blueprint, request, Response
from functools import wraps
from services.DBConn import db

userDB = db.users
auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    if not username:
        return json.dumps({'error': "Username not provided.", 'success': False, 'code': 66})
    if not password:
        return json.dumps({'error': "Password not provided.", 'success': False, 'code': 67})

    username = username.lower()
    try:
        record = userDB.find_one({'username': username})
        if record is None:
            return json.dumps({'error': "User doesn't exist.", 'success': False, 'code': 1})
        else:
            actualPassword = record['password']
            if (password == actualPassword):
                authtoken = encode_auth_token(username).decode("utf-8")
                return json.dumps({'success': True, 'token': authtoken})
            else:
                return json.dumps({'error': 'Invalid Password', 'code': 2})
    except Exception as e:
        print(e)
        return json.dumps({'error': "Server error while checking if user exists.", 'code': 3})



SECRET_KEY = "Bad Localhost Encryption Key"
if ('API_KEY' in os.environ): SECRET_KEY = os.environ['API_KEY'];


# generates an encrypted auth token using the encrypted using the secret key valid for 24 hours
def encode_auth_token(userName):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=1),
            'iat': datetime.datetime.utcnow(),
            'username': userName
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


# Decodes the auth token and returns userid as integer if token is valid or else an error as a string
def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return 'SUCCESS' + payload['username']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


# Defines the @requires_auth decoration. Any endpoint with the decoration requires authentication
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.cookies.get('barterAuth')
        if not auth_token:
            auth_token = request.headers.get('Authorization')
        if not auth_token:  # Authtoken no present so send 401
            return Response('Missing Auth Token!\n' 'You have to login with proper credentials', 401,
                            {'WWW-Authenticate': 'Basic realm="Login Required"'})

        user_name = decode_auth_token(auth_token)  # Get userid from authtoken
        if user_name.startswith('SUCCESS'):
            # set the userNameFromToken var so user can be identified form the request
            request.userNameFromToken = user_name[7:]
            # send control back to actual endpoint function
            return f(*args, **kwargs)
        else:
            return Response('\n' 'You have to login with proper credentials', 401,
                            {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

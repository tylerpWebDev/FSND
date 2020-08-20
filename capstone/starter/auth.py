import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


# udacity-capstone-castingagency
AUTH0_DOMAIN = 'udacity-capstone-castingagency.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'castingagency'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def cprint(string1, string2):
    print("=========================")
    print("")
    print(string1)
    print("")
    print(string2)
    print("")
    print("=========================")


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        print("Aborting from within get_token_auth_header")
        abort(401)

    auth_header_full = request.headers['Authorization']
    auth_header_split = auth_header_full.split(" ")

    if len(auth_header_split) != 2:
        abort(401)

    if auth_header_split[0].lower() != 'bearer':
        abort(401)

    header_token = auth_header_split[1]

    return header_token


def check_permissions(permission_name, payload):

    if 'permissions' not in payload:
        abort(400)

    if permission_name not in payload['permissions']:
        abort(403)

    return True


def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(
        f'https://udacity-capstone-castingagency.us.auth0.com/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def check_auth(permission=''):
    def check_auth_decorator(routef):
        @wraps(routef)
        def wrapper(*args1, **args2):
            token = get_token_auth_header()
            try:
                token_decode = verify_decode_jwt(token)
            except BaseException:
                abort(401)

            check_permissions(permission, token_decode)

            return routef(token, *args1, **args2)
        return wrapper
    return check_auth_decorator

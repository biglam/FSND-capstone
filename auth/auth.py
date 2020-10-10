import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
# from urllib.request import urlopen
from urllib.request import urlopen

AUTH0_DOMAIN = 'udac-capstone.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fsnd-auth'


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'authorisation_header_missing',
            'description': 'Authorisation header is expected'
        }, 401)

    split_auth_header = auth.split()
    if split_auth_header[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorisation header does not start with bearer'
        }, 401)

    elif len(split_auth_header) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(split_auth_header) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorisation header must be bearer token.'
        }, 401)

    token = split_auth_header[1]

    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'no permissions present in token'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorised',
            'description': 'unauthorised for this resource'
        }, 403)
    return True


def verify_decode_jwt(token):
    urltocheck = 'https://udac-capstone.eu.auth0.com/.well-known/jwks.json'
    jsonurl = urlopen(urltocheck)
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

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
    if rsa_key:
        try:
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

        except jwt.JWTClaimsError as e:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Claims error. Check the audience and issuer'
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


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)

            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

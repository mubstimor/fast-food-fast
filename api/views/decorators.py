""" define decorators to be used to protect endpoints. """
from functools import wraps
from flask_jwt_extended import (JWTManager, get_jwt_claims,
                                verify_jwt_in_request)
from flask import jsonify
from api import app

JWT = JWTManager(app)

@JWT.unauthorized_loader
def unauthorized_response(callback):
    """ responds to missing authorisation header. """
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header',
        'callback': callback
        }), 401

def admin_token_required(_f):
    """ create token to protect admin only routes. """
    @wraps(_f)
    def decorated(*args, **kwargs):
        """ check role = admin in user token. """
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if str(claims['roles']) != "Admin":
            return jsonify({"msg": "Admins only!"}), 403
        else:
            return _f(*args, **kwargs)
    return decorated

@JWT.user_claims_loader
def add_claims_to_access_token(identity):
    """ store user role as a claim in access token. """
    if identity['role'] == 'Admin':
        return {'roles': 'Admin'}
    else:
        return {'roles': 'Customer'}

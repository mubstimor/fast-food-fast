""" define decorators to be used to protect endpoints. """
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required,
                                get_jwt_identity, JWTManager,
                                verify_jwt_in_request)
from flask import request, jsonify
from functools import wraps
from api import app

JWT = JWTManager(app)

@JWT.unauthorized_loader
def unauthorized_response(callback):
    """ responds to missing authorisation header. """
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401

def admin_token_required(_f):
    """ create token to protect admin only routes. """
    @wraps(_f)
    def decorated(*args, **kwargs):
        """ check role = admin in user token. """
        verify_jwt_in_request()
        claims = get_jwt_identity()
        if claims['role'] != 'Admin':
            return jsonify({"msg": "Admins only!"}), 403
        else:
            return _f(*args, **kwargs)
    return decorated

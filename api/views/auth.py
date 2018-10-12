""" manage signup and login functions of the auth module. """
from flask import request, jsonify
from email_validator import validate_email, EmailNotValidError
from api.models.user import User
from api import app
from api.views.decorators import create_access_token, set_access_cookies
from flask_cors import CORS, cross_origin

USER = User()

@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
    """
        Register a new user
        ---
        tags:
          - User
        parameters:
          - in: body
            name: body
            email: body
            password: body
            gender: body
            user_type: body
            schema:
              id: User
              required:
                - name
                - email
                - password
                - gender
              properties:
                name:
                    type: string
                    description: user identifer
                email:
                    type: string
                    description: email address of user
                password:
                    type: string
                    description: secret key known to user
                gender:
                    type: string
                    description: either male or female
                user_type:
                    type: string
                    description: class of the user
                    default: Customer
        responses:
          201:
            description: New user created
    """
    gender = ('male', 'female')
    if not request.json or not 'email' in request.json:
        return jsonify({'error': True, "message": "Add 'email' parameter to request"}), 400
    try:
        validate_email(request.json['email'])
    except EmailNotValidError as _e:
        return jsonify({'error': True, "message": str(_e)}), 400
    if request.json['gender'] not in gender:
        return jsonify({'error': True, "message": "Add 'gender' parameter to request"}), 400

    user = USER.check_if_user_exists(request.json['email'])
    if user:
        return jsonify({'error': 'user already exists'}), 409
    else:
        try:
            post_user = USER.create_user(request.json)
        except KeyError:
            return jsonify({'error': True, "message": "Missing/Invalid parameters in request"}), 400
        return jsonify({'user': post_user, "message": "User successfully created."}), 201


@app.route('/api/v1/auth/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def auth_user():
    """
        Authenticate user
        ---
        tags:
          - User
        parameters:
          - in: body
            name: body
            required: true
            type: string
            description: sign in a registered user

            schema:
              id: Auth
              properties:
                email:
                    type: string
                    description: email address of user
                password:
                    type: string
                    description: secret key known to user
        responses:
          200:
            description: Login successful
    """
    if not request.json or not 'password' in request.json:
        return jsonify({'error': 'Missing password parameter in request'}), 400
    access_token = ""
    data = USER.authenticate(request.json)
    if data:
        access_token = create_access_token(identity=data)
        user = {}
        user['token'] = access_token
        user['role'] = data['role']
        response = jsonify({'ok': True, 'data': user, 'message': 'login successful'})
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify({'ok': False, 'message': 'invalid username or password'}), 401

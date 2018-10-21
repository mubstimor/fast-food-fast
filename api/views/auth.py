""" manage signup and login functions of the auth module. """
from flask import request, jsonify
from flask_cors import cross_origin
from email_validator import validate_email, EmailNotValidError
from api.models.user import User
from api import app
from api.views.decorators import create_access_token
from pprint import pprint


USER = User()

@app.route('/api/v1/auth/signup', methods=['POST'])
@cross_origin()
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
    try:
        validate_email(request.json['email'])
    except EmailNotValidError as _e:
        return jsonify({'error': True, "message": str(_e)}), 400
    if request.json['gender'] not in gender:
        return jsonify({'error': True,
                        "message": "Add 'gender' parameter to request"}), 400

    user = USER.check_if_user_exists(request.json['email'])
    if user:
        return jsonify({'message': 'user already exists', 'error':True}), 409
    else:
        post_user = USER.create_user(request.json)
        return jsonify({'user': post_user,
                        "message": "User successfully created.",
                        "error": False}), 201


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
        return jsonify({
            'error':'Missing password parameter in request'}), 400
    access_token = ""
    data = USER.authenticate(request.json)
    if data:
        pprint("USER DATA")
        pprint(data)
        access_token = create_access_token(identity=data)
        user = {}
        user['token'] = access_token
        user['role'] = data['role']
        response = jsonify({'ok': True, 'data': user,
                            'message': 'login successful'})
        response.status_code = 200

        # add token to response headers - so SwaggerUI can use it
        response.headers.extend({'jwt-token': access_token})
        return response
    else:
        return jsonify({'ok': False,
                        'message': 'invalid username or password',
                        'data':data
                        }), 401


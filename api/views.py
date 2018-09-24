""" manages routes to the app. """
# from flask import render_template
from flask import request, jsonify
from flask import abort
from flask import make_response
from flask import url_for
from api import app
from api.order import Order
from api.user import User

# Create orders list variable to store information.
# orders = []
ORDER = Order()
USER = User()

@app.route('/', methods=['GET'])
def index():
    """ route to index of the API. """
    return jsonify({'Home': 'Index of the API'})

# ROUTES FOR ORDERS.

@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    """ create order with post request. """
    if not request.json or not 'item' in request.json:
        abort(400)

    try:
        request.json['quantity'] = isinstance(int(request.json['quantity']), int)
        request.json['user_id'] = isinstance(int(request.json['user_id']), int)
    except ValueError:
        abort(400)
    return jsonify({'order': ORDER.create_order(request.json)}), 201

@app.route('/api/v1/orders', methods=['GET'])
def api_all():
    """ A route to return all of the available orders. """
    return jsonify({'orders': \
    [make_public_order(order_item) for order_item in ORDER.fetch_all_orders()]})

@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """ Get a specific order with given id."""
    order_list = ORDER.get_order(order_id)
    if not order_list:
        abort(404)
    return jsonify({'order': order_list[0]})

@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """ update order status with put request. """
    status = ("accepted", "rejected", "completed")
    if request.json['status'] not in status:
        abort(400)
    order_list = ORDER.get_order(order_id)
    if not order_list:
        abort(404)
    return jsonify({'order': ORDER.update_order(order_id, request.json)})

@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """ delete requested resource from list. """
    order_list = ORDER.get_order(order_id)
    if not order_list:
        abort(404)
    return jsonify({'result': ORDER.delete_order(order_id)})

# END ORDER ROUTES

# ROUTES FOR CUSTOMERS

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """ create user with post request. """
    gender = ('male', 'female')
    if not request.json or not 'email' in request.json:
        abort(400)
    if request.json['gender'] not in gender:
        abort(400)
    return jsonify({'user': USER.create_user((request.json))}), 201

@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    """ A route to return all of the available users. """
    return jsonify({'users': USER.fetch_all_users()})

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ Get a specific user with given id."""
    user_list = USER.get_user(user_id)
    if not user_list:
        abort(404)
    return jsonify({'user': user_list[0]})

@app.route('/api/v1/users/login', methods=['POST'])
def login_user():
    """ authenticate user. """
    if not request.json or not 'password' in request.json:
        abort(400)
    if USER.login(request.json):
        response = "success"
    else:
        response = "error"
    return jsonify({'login': response})

# END CUSTOMER ROUTES

@app.errorhandler(404)
def not_found(error):
    """ return clean response for not found resources. """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ return clean response for bad requests. """
    return make_response(jsonify({'error': 'Bad Request, \
    some parameters are either missing or invalid'}), 400)

def make_public_order(order_item):
    """ replace id with link to resource. """
    new_order = {}
    for field in order_item:
        if field == 'id':
            new_order['uri'] = url_for('get_order', order_id=order_item['id'], _external=True)
        else:
            new_order[field] = order_item[field]
    return new_order

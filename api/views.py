""" manages routes to the app. """
from flask import Flask, request, jsonify
from flask import abort
from flask import make_response
from environs import Env
from pprint import pprint
from flask import Blueprint, render_template as view, render_template
from jinja2 import TemplateNotFound
from flasgger import Swagger
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from api import app
from api.order import Order
from api.user import User
from api.fooditem import FoodItem
from api.database import DatabaseConnection
# from api.docs import views

# swagger
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "FastFoodFast API Documentation",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE"),
        ('Access-Control-Allow-Credentials', "true"),
    ]
}
swagger = Swagger(app)

# # set up the flask jwt-extended extension
env = Env()
env.read_env()
app.config['JWT_SECRET_KEY'] = env.str("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Instantiate model connection variables
ORDER = Order()
USER = User()
FOODITEM = FoodItem()

# establish database
db = DatabaseConnection()
db.create_users_table()
db.create_fooditem_table
db.create_users_table

# docs = Blueprint('docs', __name__, template_folder='templates', static_folder='static')
# @app.route('/', methods=['GET'])
# @docs.route('/', methods=['GET'])
# def index():
#     """ route to index of the API. """
#     try:
#        return render_template('index.html')
#     except TemplateNotFound:
#         abort(404)

@app.route('/', methods=['GET'])
def index():
    """ route to index of the API. """
    return jsonify({'Home': 'Index of the API', "Docs":"/apidocs"})

# ROUTES FOR ORDERS.
@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    """
        Create a new order
        Allows a customer post an order
        ---
        tags:
          - ORDER
        parameters:
          - in: body
            user_id: body
            item: body
            quantity: body
            schema:
              id: Order
              required:
                - user_id
                - item
                - quantity
              properties:
                user_id:
                  type: integer
                  description: id for customer
                  default: 1
                item:
                  type: string
                  description: ordered item
                  default: Chips
                quantity:
                  type: integer
                  description: number of items requested
                  default: 1
        responses:
          201:
            description: New order created
        """
    """ create order with post request. """
    if not request.json or not 'item' in request.json:
        abort(400)
    try:
        request.json['quantity'] = int(request.json['quantity'])
        request.json['user_id'] = int(request.json['user_id'])
    except ValueError:
        abort(400)

    order  = ORDER.check_if_order_exists(request.json['user_id'], request.json['item'], request.json['quantity'])
    if order:
        return jsonify({'error': 'Order already exists'}), 403
    else:
        return jsonify({'order': ORDER.create_order(request.json)}), 201

@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    """
    Endpoint for returning list of orders
    ---
    tags:
      - ORDER
    
    responses:
      200:
        description: All available orders
    """
    """ A route to return all of the available orders."""
    orders = ORDER.fetch_all_orders()
    if orders:
        return jsonify({'orders': orders})
    else:
        return jsonify({'orders': "No orders available"})
    
@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get single order
    ---
    tags:
      - ORDER
    produces:
      - application/json
    parameters:
      - in: path
        name: order_id
        type: int
        description: order_id to be retrieved
        required: false
    responses:
      200:
        description: The requested order
    """
    # """ Get a specific order with given id."""
    order = ORDER.get_order(order_id)
    if order:
        return jsonify({'order': order})
    else:
        return jsonify({'order': 'Order not found'}), 404
    
@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
        Update a single order's status
        ---
        tags:
          - ORDER
        parameters:
          - in: body
            status: body
            schema:
              id: Order
          - in: path
            name: order_id
            required: false
            description: The ID of the order, try 1!
            type: string
        responses:
          200:
            description: The order has been updated
            # schema:
            #   id: Order
        """
    """ update order status with put request. """
    status = ("accepted", "rejected", "completed")
    if request.json['status'] not in status:
        abort(400)
    return jsonify({'order': ORDER.update_order(order_id, request.json)})

@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """ delete requested resource from list. """
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

    user  = USER.check_if_user_exists(request.json['email'])
    if user:
        return jsonify({'error': 'user already exists'}), 403
    else:
        return jsonify({'user': USER.create_user((request.json))}), 201

@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    """ A route to return all of the available users. """
    return jsonify({'users': USER.fetch_all_users()})

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ Get a specific user with given id."""
    user = USER.get_user(user_id)
    return jsonify({'user': user})

# create tokens to be used for accessing app
@app.route('/api/v1/users/login', methods=['POST'])
def login_user():
    """ authenticate user. """
    if not request.json or not 'password' in request.json:
        abort(400)
    access_token = "" # set an empty token
    if USER.login(request.json):
        # create token here
        access_token = create_access_token(identity=request.json['email'])
        # pprint(access_token)
    # return jsonify({'login': USER.login(request.json)})
    # current_user = get_jwt_identity()
    return jsonify({'login': USER.login(request.json), "access_token": access_token}), 200

@app.route('/api/v1/users/orders/<int:order_id>', methods=['PUT'])
def update_user_order(order_id):
    """ update order details with put request. """
    return jsonify({'order': ORDER.update_user_order(order_id, request.json)})

@app.route('/api/v1/users/myorders/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """ Get orders for a specific user."""
    return jsonify({'myorders': ORDER.fetch_user_orders(user_id)})
# END CUSTOMER ROUTES

# ROUTES FOR FOOD ITEMS.
@app.route('/api/v1/fooditems', methods=['POST'])
def create_fooditem():
    """ create item with post request. """
    try:
        request.json['price'] = int(request.json['price'])
    except ValueError:
        abort(400)
    
    item  = FOODITEM.check_if_item_exists(request.json['name'])
    if item:
        return jsonify({'error': 'Menu Item already exists'}), 403
    else:
        return jsonify({'fooditem': FOODITEM.create_item(request.json)}), 201

@app.route('/api/v1/fooditems', methods=['GET'])
def get_all_fooditems():
    """ A route to return all of the available fooditems. """
    return jsonify({'fooditems': FOODITEM.fetch_all_fooditems()})

@app.route('/api/v1/fooditems/<int:item_id>', methods=['GET'])
def get_fooditem(item_id):
    """ Get a specific item with given id."""
    item = FOODITEM.get_item(item_id)
    return jsonify({'fooditem': item})

@app.route('/api/v1/fooditems/<int:item_id>', methods=['PUT'])
def update_fooditem(item_id):
    """ update food item with put request. """
    return jsonify({'fooditem': FOODITEM.update_item(item_id, request.json)})

@app.route('/api/v1/fooditems/<int:item_id>', methods=['DELETE'])
def delete_fooditem(item_id):
    """ delete requested resource from list. """
    return jsonify({'result': FOODITEM.delete_item(item_id)})    
# END FOOD ITEM ROUTES

# protected decorator
@app.route('/api/v1/protected', methods=['GET'])
@jwt_required
def protected():
    # access identity of current user
    current_user = get_jwt_identity()
    # pprint("user = ")
    # pprint(current_user)
    return jsonify(logged_in_as=current_user), 200

# @app.errorhandler(404)
# def not_found(error):
#     """ return clean response for not found resources. """
#     return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ return clean response for bad requests. """
    return make_response(jsonify(
        {'error': 'Bad Request, some parameters are either missing or invalid'}), 400)


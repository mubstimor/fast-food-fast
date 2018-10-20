""" handles routes for user actions. """
from flask_cors import CORS, cross_origin
from api.models.user import User
from api.models.order import Order
from api import app
from api.views.decorators import *

USER = User()
ORDER = Order()

@app.route('/api/v1/users/orders', methods=['GET'])
@jwt_required
@cross_origin()
def get_user_orders():
    """
    Get orders for a specific user.
    ---
    tags:
      - ORDER
    produces:
      - application/json
    responses:
      200:
        description: Displays a users order history
    security:
        -JWT:
            descript: send token
            type: apiKey
            scheme: bearer
            name: access-token
            in: header
            bearerFormat: JWT
    """
    current_user = get_jwt_identity()
    get_orders = ORDER.fetch_user_orders(current_user['id'])
    return jsonify({'myorders': get_orders})

@app.route('/api/v1/users/orders/<int:order_id>', methods=['GET'])
@jwt_required
@cross_origin()
def get_single_user_order(order_id):
    """ get single client's order, 
    check both user id and the order id passed."""
    current_user = get_jwt_identity()
    get_order = ORDER.fetch_user_order(order_id, current_user['id'])
    return jsonify({'order': get_order, 'error': False,
                    'message': 'order retrieved.'})

@app.route('/api/v1/users/orders', methods=['POST'])
@jwt_required
def create_order():
    """
        Create a new order
        Allows a customer post an order
        ---
        tags:
          - ORDER
        parameters:
          - in: body
            item: body
            quantity: body
            schema:
              id: Order
              required:
                - item
                - quantity
              properties:
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
    if not request.json or not 'item' in request.json:
        return jsonify({'message': 'Missing Item parameter in request', 'error': True}), 400

    try:
        int(request.json['quantity'])
    except ValueError:
        return jsonify({'message': 'Invalid quantity value', 'error': True}), 400

    current_user = get_jwt_identity()
    logged_in_user = current_user['id']

    order = ORDER.check_if_order_exists(logged_in_user,
                                        request.json['item'],
                                        request.json['quantity'])
    if order:
        return jsonify({'message': 'A recent similar order already exists, would you rather simply update it?',
                        'error': True}), 409
    else:
        create_user_order = ORDER.create_order(logged_in_user, request.json)
        return jsonify({"message":"Order successfully created",
                        'id': create_user_order, 'error': False}), 201

@app.route('/api/v1/users/orders/<int:order_id>', methods=['PUT'])
@jwt_required
def update_user_order(order_id):
    """ update order details with put request. """
    return jsonify({'order': ORDER.update_user_order(order_id, request.json),
                    'error': False, 'message': 'Order Updated Successfully'})

@app.route('/api/v1/users/orders/cancel/<int:order_id>', methods=['PUT'])
@jwt_required
@cross_origin()
def cancel_user_order(order_id):
    """ cancel user order with put request. """
    return jsonify({'order': ORDER.update_order(order_id, request.json),
                    'error': False, 'message': 'Order Cancelled Successfully'})

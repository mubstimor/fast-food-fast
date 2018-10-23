""" managaes access operations on order objects. """
from flask_cors import cross_origin
from api.models.order import Order
from api import app
from api.views.decorators import (request, jsonify,
                                  admin_token_required, jwt_required,
                                  get_jwt_identity)

ORDER = Order()

@app.route('/api/v1/orders', methods=['GET'])
@jwt_required
@cross_origin()
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
    user = get_jwt_identity()
    if user['role'] != 'Admin':
        return jsonify({'message': "Unauthorised to access this area", 'error': True}), 403

    orders = ORDER.fetch_all_orders()
    if orders:
        return jsonify({'orders': orders, 'error': False})
    else:
        return jsonify({'orders': "No orders available", 'error': False})

@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
@jwt_required
@cross_origin()
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
    user = get_jwt_identity()
    if user['role'] != 'Admin':
        return jsonify({'message': "Unauthorised to access this area", 'error': True}), 403

    order = ORDER.get_order(order_id)
    if order:
        return jsonify({'order': order})
    else:
        return jsonify({'order': 'Order not found'}), 404

@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
@admin_token_required
@cross_origin()
def update_order(order_id):
    """
        Update a single order's status
        ---
        tags:
          - ORDER
        schemes:
          - bearer

        securityDefinitions:
          api_key:
            type: apiKey
            name: api_key
            in: header
            description: Requests should pass an api_key header.

        security:
          - api_key: []

        parameters:
          - in: path
            name: order_id
            required: false
            description: The ID of the order, try 1!
            type: integer
          - in: body
            name: body
            schema:
              id: Status
              properties:
                name:
                    type: string
                    description: state of order
                    default: New
        responses:
          200:
            description: The order has been updated
        """
    status = ("processing", "cancelled", "complete")
    if request.json['name'] not in status:
        return jsonify({'message': 'Missing status parameter in request',
                        'error': True}), 400
    return jsonify({'order': ORDER.update_order(order_id, request.json),
                    'message': 'Order successfully updated', 'error': False})

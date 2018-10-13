""" managaes access operations on order objects. """
from flask_cors import cross_origin
from api.models.order import Order
from api import app
from api.views.decorators import *

ORDER = Order()

@app.route('/api/v1/orders', methods=['GET', 'OPTIONS'])
@jwt_required
@admin_token_required
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
    get_jwt_identity()
    orders = ORDER.fetch_all_orders()
    if orders:
        return jsonify({'orders': orders})
    else:
        return jsonify({'orders': "No orders available"})

@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
@admin_token_required
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
    status = ("processing", "cancelled", "complete")
    if request.json['status'] not in status:
        return jsonify({'error': 'Missing status parameter in request'}), 400
    return jsonify({'order': ORDER.update_order(order_id, request.json)})

@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
@admin_token_required
@cross_origin()
def delete_order(order_id):
    """ delete requested resource from list. """
    return jsonify({'result': ORDER.delete_order(order_id)})

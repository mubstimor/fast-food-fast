from api.order import Order
from api import app
from api.views.decorators import *

ORDER = Order()


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
        return jsonify({'error': 'Missing Item parameter in request'}), 400
    try:
        request.json['quantity'] = int(request.json['quantity'])
    except ValueError:
        return jsonify({'error': 'Bad request'}), 400

    current_user = get_jwt_identity()
    logged_in_user = current_user['id']

    order = ORDER.check_if_order_exists(logged_in_user , \
                                        request.json['item'], request.json['quantity'])
    if order:
        return jsonify({'error': 'Order already exists'}), 409
    else:
        create_user_order = ORDER.create_order(logged_in_user, request.json)
        if create_user_order:
            return jsonify({"message":"Order successfully created",
                            'id': create_user_order}), 201
        else:
            return jsonify({'error': True, "message":"Unable to support request"}), 400


@app.route('/api/v1/orders', methods=['GET'])
@admin_token_required
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
    orders = ORDER.fetch_all_orders()
    if orders:
        return jsonify({'orders': orders})
    else:
        return jsonify({'orders': "No orders available"})
  
@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
@admin_token_required
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
def delete_order(order_id):
    """ delete requested resource from list. """
    return jsonify({'result': ORDER.delete_order(order_id)})

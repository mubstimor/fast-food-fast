from api.models.user import User
from api.models.order import Order
from api import app
from api.views.decorators import *

USER = User()
ORDER = Order()

@app.route('/api/v1/users/orders', methods=['GET'])
@jwt_required
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
    if get_user_orders:
        return jsonify({'myorders': get_orders})
    else:
        return jsonify({"message":"no orders available for current user"})


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

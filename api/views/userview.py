from api.user import User
from api.order import Order
from api import app
from api.views.decorators import *

USER = User()
ORDER = Order()

@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    """ A route to return all of the available users. """
    return jsonify({'users': USER.fetch_all_users()})

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ Get a specific user with given id."""
    user = USER.get_user(user_id)
    return jsonify({'user': user})

@app.route('/api/v1/users/orders/<int:order_id>', methods=['PUT'])
def update_user_order(order_id):
    """ update order details with put request. """
    return jsonify({'order': ORDER.update_user_order(order_id, request.json)})

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

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def elevate_user_to_admin(user_id):
    """ update user to admin. """
    status = USER.assign_admin_privileges(user_id)
    return jsonify(status)

@app.route('/api/v1/users/admin/<string:email>', methods=['GET'])
def get_user_data(email):
    """ Get orders for a specific user."""
    data = USER.get_user_data_from(email)
    return jsonify(data)

from api import app
from api.models.fooditem import FoodItem
from api.views.decorators import *
from api.models.user import User
from api.models.order import Order

FOODITEM = FoodItem()
USER = User()
ORDER = Order()

@app.route('/api/v1/menu/<int:item_id>', methods=['GET'])
def get_fooditem(item_id):
    """
    Get single menu item
    ---
    tags:
      - MENU
    produces:
      - application/json
    parameters:
      - in: path
        name: item_id
        type: int
        description: item_id to be retrieved
        required: false
    responses:
      200:
        description: The requested menu item
    """
    item = FOODITEM.get_item(item_id)
    return jsonify({'fooditem': item})

@app.route('/api/v1/menu/<int:item_id>', methods=['PUT'])
@admin_token_required
def update_fooditem(item_id):
    """ update food item with put request. """
    return jsonify({'fooditem': FOODITEM.update_item(item_id, request.json)})

@app.route('/api/v1/menu/<int:item_id>', methods=['DELETE'])
def delete_fooditem(item_id):
    """ delete requested resource from list. """
    return jsonify({'result': FOODITEM.delete_item(item_id)})

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
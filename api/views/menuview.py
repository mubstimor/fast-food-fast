from api import app
from api.fooditem import FoodItem
from api.views.decorators import *

FOODITEM = FoodItem()

@app.route('/api/v1/menu', methods=['POST'])
@admin_token_required
def create_fooditem():
    """
        Create a new menu item
        Allows an admin to post a food item
        ---
        tags:
          - MENU
        securityDefinitions:
            bearerAuth:
                type: bearer
        parameters:
          - in: body
            name: body
            category: body
            price: body
            schema:
              id: Menu
              required:
                - name
                - category
                - price
              properties:
                name:
                    type: string
                    description: description of food item
                    default: 1
                category:
                    type: string
                    description: class to which the item belongs
                    default: Foods
                price:
                    type: integer
                    description: monetary worth of item
                    default: 3000
        responses:
          201:
            description: New order created
        # openapi: 3.0.0
        components:
            securitySchemes:
                bearerAuth:
                    type: apiKey
                    scheme: bearer
                    in: header
                    bearerFormat: JWT
        security:
            - bearerAuth: []            
    """
    try:
        request.json['price'] = int(request.json['price'])
    except ValueError:
        return jsonify({'error': 'Invalid price value'}), 400

    item = FOODITEM.check_if_item_exists(request.json['name'])
    if item:
        return jsonify({'error': 'Menu Item already exists'}), 409
    else:
        return jsonify({'fooditem': FOODITEM.create_item(request.json)}), 201

@app.route('/api/v1/menu', methods=['GET'])
def get_all_fooditems():
    """
    Get available menu
    ---
    tags:
      - MENU
    produces:
      - application/json
    responses:
      200:
        description: Displays a list of available menu item
    """
    return jsonify({'menu': FOODITEM.fetch_all_fooditems()})

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
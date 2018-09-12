""" manages routes to the app. """
# from flask import render_template
from flask import request, jsonify
from flask import abort
from flask import make_response
from flask import url_for
from api import app
from api.order import Order

# Create orders list variable to store information.
# orders = []
order = Order()

@app.route('/', methods=['GET'])
def index():
    """ route to index of the API. """
    return jsonify({'Home': 'Index of the API'})

@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    """ create order with post request. """
    if not request.json or not 'item' in request.json:
        abort(400)
    return jsonify({'order': order.create_order(request.json)}), 201


@app.route('/api/v1/orders', methods=['GET'])
def api_all():
    """ A route to return all of the available orders. """
    return jsonify({'orders': \
    [make_public_order(order_item) for order_item in order.fetch_all_orders()]})

@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """ Get a specific order with given id."""
    order_list = order.get_order(order_id)
    if not order_list:
        abort(404)
    return jsonify({'order': order_list[0]})

@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """ update resource with put request. """
    order_list = order.get_order(order_id)
    if not order_list:
        abort(404)
    if not request.json:
        abort(400)
    return jsonify({'order': order.update_order(order_id, request.json)})

@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """ delete requested resource from list. """
    order_list = order.get_order(order_id)
    if not order_list:
        abort(404)
    return jsonify({'result': order.delete_order(order_id)})

@app.errorhandler(404)
def not_found(error):
    """ return clean response for not found resources. """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ return clean response for bad requests. """
    return make_response(jsonify({'error': 'Bad Request'}), 400)

def make_public_order(order_item):
    """ replace id with link to resource. """
    new_order = {}
    for field in order_item:
        if field == 'id':
            new_order['uri'] = url_for('get_order', order_id=order_item['id'], _external=True)
        else:
            new_order[field] = order_item[field]
    return new_order

""" manages routes to the app. """
# from flask import render_template
from flask import request, jsonify
from flask import abort
from flask import make_response
from flask import url_for
from api import app
# from api.models import Order

# Create orders list variable to store information.
orders = []

@app.route('/', methods=['GET'])
def index():
    """ route to index of the API. """
    return jsonify({'Home': 'Index of the API'})

@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    """ create order with post request. """
    if not request.json or not 'item' in request.json:
        abort(400)
    order = {
        'id': len(orders) + 1,
        'item': request.json['item'],
        'quantity': request.json['quantity'],
        'user_id': request.json['user_id']
    }
    orders.append(order)
    return jsonify({'order': order}), 201


@app.route('/api/v1/orders', methods=['GET'])
def api_all():
    """ A route to return all of the available orders. """
    return jsonify({'orders': [make_public_order(order) for order in orders]})

@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """ Get a specific order with given id."""
    order = [order for order in orders if order['id'] == order_id]
    if not order:
        abort(404)
    return jsonify({'order': order[0]})


@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """ update resource with put request. """
    order = [order for order in orders if order['id'] == order_id]
    if not order:
        abort(404)
    if not request.json:
        abort(400)
    if 'item' not in request.json:
        abort(400)
    if 'quantity' not in request.json:
        abort(400)
    if 'user_id' not in request.json:
        abort(400)
    order[0]['item'] = request.json.get('item', order[0]['item'])
    order[0]['quantity'] = request.json.get('quantity', order[0]['quantity'])
    order[0]['user_id'] = request.json.get('user_id', order[0]['user_id'])
    return jsonify({'order': order[0]})

@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """ delete requested resource from list. """
    order = [order for order in orders if order['id'] == order_id]
    if not order: # if order is empty
        abort(404)
    orders.remove(order[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    """ return clean response for not found resources. """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ return clean response for bad requests. """
    return make_response(jsonify({'error': 'Bad Request'}), 400)

def make_public_order(order):
    """ replace id with link to resource. """
    new_order = {}
    for field in order:
        if field == 'id':
            new_order['uri'] = url_for('get_order', order_id=order['id'], _external=True)
        else:
            new_order[field] = order[field]
    return new_order

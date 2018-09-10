# from flask import render_template
import flask
from flask import request, jsonify
from flask import abort
from flask import make_response
from flask import url_for
from api import models

from api import app

@app.route('/',  methods=['GET'])
def index():
	return jsonify({'Home': 'Index of the API'})

# Create some test data for orders in the form of a list of dictionaries.
orders = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# create task with post request
@app.route('/api/orders', methods=['POST'])
def create_order():
    if not request.json or not 'user' in request.json:
        abort(400)
    task = {
        'id': orders[-1]['id'] + 1,
        'user': request.json['user'],
        # 'description': request.json.get('description', ""),
        # 'done': False
    }
    
    return jsonify(request.json), 201

# A route to return all of the available orders.
@app.route('/api/v1/orders', methods=['GET'])
def api_all():
    return jsonify({'orders': [make_public_task(task) for task in tasks]})

# Get a specific task with given id
@app.route('/api/v1/orders/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# create task with post request
@app.route('/api/v1/orders', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': orders[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    orders.append(task)
    return jsonify({'task': task}), 201

@app.route('/api/v1/orders/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in orders if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/api/v1/orders/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in orders if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    orders.remove(task[0])
    return jsonify({'result': True})

# Specify error message
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404) 

# improve url
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

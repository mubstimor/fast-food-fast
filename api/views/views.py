""" manages routes to the app. """
from flask import request, jsonify
from environs import Env
from pprint import pprint
from api import app
from api.models.order import Order
from api.models.user import User
from api.models.fooditem import FoodItem
from api.views.decorators import *

ORDER = Order()
USER = User()
FOODITEM = FoodItem()

@app.route('/', methods=['GET'])
def index():
    """ route to index of the API. """
    return jsonify({'Home': 'Index of the API', "Docs":"/apidocs"})

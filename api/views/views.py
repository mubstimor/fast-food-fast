""" manages routes to the app. """
from flask import request, jsonify
from environs import Env
from pprint import pprint
from api import app
from api.models.order import Order
from api.models.user import User
from api.models.fooditem import FoodItem
from api.views.decorators import *
from flask import Blueprint, render_template as view
from jinja2 import TemplateNotFound

ORDER = Order()
USER = User()
FOODITEM = FoodItem()

# frontend = Blueprint('frontend', __name__, template_folder='ui')
@app.route('/', methods=['GET'])
# @frontend.route('/')
def index():
    """ route to index of the API. """
    return jsonify({'Home': 'Index of the API', "Docs":"/apidocs"})
    # return view('index.html')
    # try:
    #    return view('frontend/index.html')
    # except TemplateNotFound as e:
    #     return jsonify({'error': "template not found "+ str(e)})

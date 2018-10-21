""" Initialize the app """
import datetime
from flask import Flask
from flasgger import Swagger
from environs import Env
from flask_cors import CORS
from api.db.database import DatabaseConnection

app = Flask(__name__, instance_relative_config=True)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'Authorization'
app.config['CORS_HEADERS'] = 'Origin'

from api.views import views, auth, orderview, userview, menuview
app.config.from_object('config')

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "FastFoodFast API Documentation",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ]
}
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
SWAGGER = Swagger(app)
ENV = Env()
ENV.read_env()
app.config['SECRET_KEY'] = ENV.str("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

_db = DatabaseConnection()
_db.create_all_tables()

@app.after_request
def after_request(response):
    """ override acceptable methods """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
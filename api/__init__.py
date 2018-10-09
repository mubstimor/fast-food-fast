""" Initialize the app """
import datetime
from flask import Flask
from flasgger import Swagger
from environs import Env

app = Flask(__name__, instance_relative_config=True)

from api.views import views, auth, orderview, userview, menuview, extraviews
app.config.from_object('config')

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "FastFoodFast API Documentation",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE"),
        ('Access-Control-Allow-Credentials', "true"),
    ]
}
SWAGGER = Swagger(app)
ENV = Env()
ENV.read_env()
app.config['SECRET_KEY'] = ENV.str("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


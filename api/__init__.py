""" Initialize the app """
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

from api import views
# Load the config file
app.config.from_object('config')

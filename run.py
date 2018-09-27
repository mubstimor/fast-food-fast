""" opens the app for running """
from api import app
from flask import Flask

# app = Flask(__name__)
# app.config.from_object("config")

if __name__ == '__main__':
    app.run()

from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__, template_folder='ui')


@frontend.route('/')
def home():
    """
    Show an index template
    :return:
    """
    return render_template('frontend/index.html')
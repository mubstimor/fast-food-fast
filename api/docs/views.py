from flask import Blueprint, render_template as view, render_template

docs = Blueprint('docs', __name__, static_folder='static', template_folder='templates')


@docs.route('/')
def home():
    """
    Show an index template
    :return:
    """
    # return view('docs/index.html')
    return render_template('docs/index.html', name='Tim')

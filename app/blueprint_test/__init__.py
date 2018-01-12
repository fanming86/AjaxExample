from flask import Blueprint,render_template

mmm = Blueprint('main',__name__)


@mmm.route('/hello')
def hello():
    return render_template('test.html')
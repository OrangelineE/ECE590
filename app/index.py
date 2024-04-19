from flask import render_template, request, Blueprint
bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')
# __init__.py
from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB
from .models.patient import Patient 
from .notification import setup_scheduler

login = LoginManager()
login.login_view = 'patients.login'

@login.user_loader
def load_user(user_id):
    return Patient.get_by_id(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.db = DB(app)
    login.init_app(app)
    from .index import bp as index_bp
    app.register_blueprint(index_bp)
    from .patients import bp as user_bp
    app.register_blueprint(user_bp)
    from .slots import bp as slot_bp
    app.register_blueprint(slot_bp)
    from .reminders import bp as reminders_bp
    app.register_blueprint(reminders_bp)
    setup_scheduler(app)
    return app

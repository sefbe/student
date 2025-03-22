from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routes import payment_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Initialisation de Flask-Migrate
    migrate = Migrate(app, db)

    app.register_blueprint(payment_bp)

    return app


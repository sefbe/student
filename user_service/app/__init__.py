from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate  # Ajout de Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()  # Initialisation de Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Initialisation de Migrate avec l'application et la base de données

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    from app.routes import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/api/users")

    from app.admin_routes import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/api/admin")

    # Crée les tables si elles n'existent pas encore
    with app.app_context():
        db.create_all()  # Crée les tables de la base de données

    return app

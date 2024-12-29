from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configure le gestionnaire de connexion
    login_manager.login_view = "user.login"  # Route pour la page de connexion
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."

    # Définir la fonction user_loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import tardif pour éviter les dépendances circulaires
        return User.query.get(int(user_id))

    from app.routes import room_bp
    app.register_blueprint(room_bp, url_prefix='/api/rooms')

    return app

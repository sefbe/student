### apigateway/app/__init__.py
##from flask import Flask
##from flask_login import LoginManager
##import requests

# Initialisation des extensions
##login_manager = LoginManager()

##def create_app():
##    app = Flask(__name__)
##    
##    # Importer la configuration depuis le fichier config.py
##    app.config.from_object('app.config.Config')
##
##    # Initialisation de Flask-Login
##    login_manager.init_app(app)
##
##    # Configuration du gestionnaire de connexion
##    login_manager.login_view = "app_bp.login"
##    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
##
##    @login_manager.user_loader
##    def load_user(user_id):
##        try:
##            response = requests.get(f"{USER_SERVICE_URL}/api/users/{user_id}")
##            if response.status_code == 200:
##                user_data = response.json()
##                return user_data  # Assurez-vous que cela correspond à la structure de l'utilisateur que vous attendez
##            return None
##        except requests.RequestException:
##            return None
##
##    from app.routes import app_bp
##    app.register_blueprint(app_bp, url_prefix='/')
##
##    return app
from flask import Flask
from flask_login import LoginManager
import requests
from app.models import User

# Initialisation des extensions
login_manager = LoginManager()
USER_SERVICE_URL = "http://127.0.0.1:5001" 
# Définition de la fonction load_user en dehors de create_app
@login_manager.user_loader
def load_user(user_id):
    try:
        response = requests.get(f"{USER_SERVICE_URL}/api/users/{user_id}")
        if response.status_code == 200:
            user_data = response.json()
            user = User(user_data['id'], user_data['username'], user_data['email'], user_data['first_name'], user_data['last_name'], user_data['status'])
            return user  # Assurez-vous que cela correspond à la structure de l'utilisateur que vous attendez
        return None
    except requests.RequestException:
        return None

def create_app():
    app = Flask(__name__)
    
    # Importer la configuration depuis le fichier config.py
    app.config.from_object('app.config.Config')

    # Initialisation de Flask-Login
    login_manager.init_app(app)

    # Configuration du gestionnaire de connexion
    login_manager.login_view = "app_bp.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."

    from app.routes import app_bp
    app.register_blueprint(app_bp, url_prefix='/')

    return app

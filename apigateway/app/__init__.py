from flask import Flask
from flask_login import LoginManager
import requests
from app.models import User

# Initialiser Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'api311937Sefa@'
    
    # Initialiser Flask-Login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Cette fonction sera utilisée par Flask-Login pour charger un utilisateur
        à partir de l'ID. Elle interroge le microservice user_service pour récupérer
        les informations de l'utilisateur.
        """
        try:
            # Interroger le microservice `user_service` pour récupérer les informations de l'utilisateur
            response = requests.get(f"http://127.0.0.1:5001/api/users/{user_id}")
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Créer un objet User fictif avec les données reçues
                user = User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    status=user_data['status']
                )
                return user
            else:
                # Si l'utilisateur n'est pas trouvé, retourner un utilisateur fictif pour les tests
                return User(id=user_id, username="fictif", email="fictif@example.com", first_name="Fictif", last_name="Utilisateur", status="test")
        except requests.exceptions.RequestException as e:
            # Gérer les erreurs de connexion avec le microservice
            print(f"Erreur de connexion au service utilisateur: {e}")
            return None

    # Enregistrer les blueprints pour les différentes routes
    from app.routes import app_bp
    app.register_blueprint(app_bp)

    return app

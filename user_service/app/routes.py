from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/status", methods=["GET"])
@login_required
def user_status():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'status': current_user.status
    }), 200


# Récupérer un utilisateur par son ID
@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        # Si l'utilisateur est trouvé, renvoyer ses informations sous forme de JSON
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'status': user.status,
            'is_active': user.is_active
        }), 200
    else:
        # Si l'utilisateur n'est pas trouvé, renvoyer une erreur 404
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

@user_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return jsonify({"message": "Veuillez envoyer vos données d'inscription via POST"}), 405  # Méthode non autorisée

    if request.method == "POST":
        data = request.json
        if not all(k in data for k in ("username", "email", "password", "first_name", "last_name", "status")):
            return jsonify({"message": "Données manquantes"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        status = data.get("status")

        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            return jsonify({"message": "Email ou nom d'utilisateur déjà existant"}), 400

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            status=status,
        )
        user.set_password(password)  # Assurez-vous que cette méthode hache le mot de passe
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Utilisateur enregistré avec succès"}), 201

# Connexion (GET, POST)
@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return jsonify({"message": "Veuillez envoyer vos informations de connexion via POST"}), 200

    if request.method == "POST":
        if current_user.is_authenticated:
            return jsonify({"message": "Déjà connecté"}), 200

        data = request.json
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"message": "Identifiants invalides"}), 401

        login_user(user)
        # Générer un token ici (par exemple, avec JWT)
        from app.utils.token_utils import generate_token
        token = generate_token(user.id)  # Remplacez par votre méthode pour générer le token
        return jsonify({"message": "Connexion réussie", "token": token, "user_id": user.id}), 200

# Déconnexion
@user_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Déconnexion réussie"}), 200


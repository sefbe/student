from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

user_blueprint = Blueprint("user", __name__)

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
            'status': user.status
        }), 200
    else:
        # Si l'utilisateur n'est pas trouvé, renvoyer une erreur 404
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

# Inscription (GET, POST)
@user_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return jsonify({"message": "Veuillez envoyer vos données d'inscription via POST"}), 200

    if request.method == "POST":
        data = request.json
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
        user.set_password(password)
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
        return jsonify({"message": "Connexion réussie"}), 200

# Déconnexion
@user_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Déconnexion réussie"}), 200


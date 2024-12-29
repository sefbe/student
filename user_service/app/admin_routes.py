from flask import Blueprint, request, jsonify
from flask_login import login_required
from app import db
from app.models import User

admin_blueprint = Blueprint("admin", __name__)

# Supprimer un utilisateur
@admin_blueprint.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({"message": "Accès interdit"}), 403

    user = User.query.get(user_id)
    if user:
        user.is_deleted = True
        db.session.commit()
        return jsonify({"message": "Utilisateur supprimé avec succès"}), 200
    return jsonify({"message": "Utilisateur non trouvé"}), 404

# Suspendre un utilisateur
@admin_blueprint.route("/suspend_user/<int:user_id>", methods=["POST"])
@login_required
def suspend_user(user_id):
    if not current_user.is_admin:
        return jsonify({"message": "Accès interdit"}), 403

    data = request.json
    period_days = data.get("period_days")

    user = User.query.get(user_id)
    if user:
        user.suspend(period_days)
        return jsonify({"message": f"Utilisateur suspendu pour {period_days} jours"}), 200
    return jsonify({"message": "Utilisateur non trouvé"}), 404

# Réintégrer un utilisateur supprimé
@admin_blueprint.route("/restore_user/<int:user_id>", methods=["POST"])
@login_required
def restore_user(user_id):
    if not current_user.is_admin:
        return jsonify({"message": "Accès interdit"}), 403

    user = User.query.get(user_id)
    if user:
        user.restore()
        return jsonify({"message": "Utilisateur réintégré avec succès"}), 200
    return jsonify({"message": "Utilisateur non trouvé"}), 404


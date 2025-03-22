from flask import Blueprint, request, jsonify, flash, redirect, url_for
from app.models import Payment, db

payment_bp = Blueprint('payment_bp', __name__)

# Ajouter un paiement
@payment_bp.route('/payments', methods=['POST'])
def add_payment():
    try:
        payer_id = request.json.get('payer_id')
        room_id = request.json.get('room_id')

        if not payer_id or not room_id:
            return jsonify({"message": "payer_id et room_id sont requis"}), 400

        new_payment = Payment(payer_id=payer_id, room_id=room_id)
        db.session.add(new_payment)
        db.session.commit()

        return jsonify({"message": "Paiement ajouté avec succès", "payment": new_payment.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erreur lors de l'ajout du paiement: {str(e)}"}), 500

# Supprimer un paiement
@payment_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    try:
        payment = Payment.query.get_or_404(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return jsonify({"message": "Paiement supprimé avec succès"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erreur lors de la suppression du paiement: {str(e)}"}), 500

# Récupérer tous les paiements
@payment_bp.route('/payments', methods=['GET'])
def get_all_payments():
    try:
        payments = Payment.query.all()
        return jsonify([payment.to_dict() for payment in payments]), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération des paiements: {str(e)}"}), 500


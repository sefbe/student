from flask import Blueprint, request, jsonify
from app.models import Reservation, db

reservation_bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@reservation_bp.route('/add', methods=['POST'])
def add_reservation():
    data = request.get_json()
    user_id = data.get('user_id')
    room_id = data.get('room_id')

    if not user_id or not room_id:
        return jsonify({'error': 'Missing required fields'}), 400

    reservation = Reservation(user_id=user_id, room_id=room_id)
    db.session.add(reservation)
    db.session.commit()

    return jsonify({'message': 'Reservation added successfully', 'reservation': str(reservation)}), 201

@reservation_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    reservation = Reservation.query.get(id)

    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404

    db.session.delete(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation deleted successfully'}), 200

@reservation_bp.route('/all', methods=['GET'])
def get_all_reservations():
    reservations = Reservation.query.all()
    return jsonify([{
        "id": r.id,
        "user_id": r.user_id,
        "room_id": r.room_id,
        "reservation_date": r.reservation_date.strftime('%Y-%m-%d %H:%M:%S')
    } for r in reservations]), 200

@reservation_bp.route('/get/<int:id>', methods=['GET'])
def get_reservation(id):
    reservation = Reservation.query.get(id)

    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404

    return jsonify({
        "id": reservation.id,
        "user_id": reservation.user_id,
        "room_id": reservation.room_id,
        "reservation_date": reservation.reservation_date.strftime('%Y-%m-%d %H:%M:%S')
    }), 200


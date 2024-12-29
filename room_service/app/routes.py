from flask import Blueprint, request, jsonify
from app import db
from app.models import Room
import random

room_bp = Blueprint('room_bp', __name__)

@room_bp.route('/random', methods=['GET'])
def get_random_rooms():
    rooms = Room.query.all()
    if not rooms:  # Vérifie si la liste est vide
        return jsonify([]), 200  # Retourne une liste vide avec un statut 200 OK

    # Sélectionne au maximum 3 chambres aléatoires
    random_rooms = random.sample(rooms, min(len(rooms), 3))
    return jsonify([room.to_dict() for room in random_rooms]), 200


@room_bp.route('/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = Room.query.get_or_404(room_id)
    return jsonify(room.to_dict())

@room_bp.route('/', methods=['POST'])
def add_room():
    data = request.get_json()
    new_room = Room(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        location=data['location'],
        distance=data['distance'],
        images=data['images']
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify(new_room.to_dict()), 201

@room_bp.route('/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Chambre supprimée"}), 200


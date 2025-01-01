from flask import Blueprint, request, jsonify
from app import db
from app.models import Room, Image
import random
import base64  # Pour encoder/décoder les images en base64


room_bp = Blueprint('room_bp', __name__)

@room_bp.route('/random', methods=['GET'])
def get_random_rooms():
    rooms = Room.query.all()
    if not rooms:
        return jsonify([]), 200

    random_rooms = random.sample(rooms, min(len(rooms), 3))
    result = []
    for room in random_rooms:
        room_data = room.to_dict()
        room_data['images'] = [
            {"name": image.image_name, "data": base64.b64encode(image.image_data).decode('utf-8')}
            for image in room.images
        ]
        result.append(room_data)
    return jsonify(result), 200


@room_bp.route('/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = Room.query.get_or_404(room_id)
    images = [
        {"name": image.image_name, "data": base64.b64encode(image.image_data).decode('utf-8')}
        for image in room.images
    ]
    room_data = room.to_dict()
    room_data['images'] = images
    return jsonify(room_data)



@room_bp.route('/', methods=['POST'])
def add_room():
    data = request.get_json()

    required_fields = ['title', 'description', 'price', 'location', 'distance', 'owner_id', 'images', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Données manquantes"}), 400

    # Crée une nouvelle chambre
    new_room = Room(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        location=data['location'],
        distance=data['distance'],
        owner_id=data['owner_id'],
        status=data['status']
    )
    try:
        db.session.add(new_room)
        db.session.flush()  # Permet d'obtenir l'ID de la chambre avant commit

        # Ajout des images associées
        for image_base64 in data['images']:
            image_data = base64.b64decode(image_base64['data'])  # Décoder l'image
            new_image = Image(
                room_id=new_room.id,
                image_data=image_data,
                image_name=image_base64['name']
            )
            db.session.add(new_image)

        db.session.commit()
        return jsonify(new_room.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'ajout de la chambre : {str(e)}")
        return jsonify({"message": "Erreur lors de l'ajout de la chambre", "error": str(e)}), 500


@room_bp.route('/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    try:
        db.session.delete(room)
        db.session.commit()
        return jsonify({"message": "Chambre supprimée"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'ajout de la chambre : {str(e)}")
        return jsonify({"message": "Erreur lors de la suppression de la chambre", "error": str(e)}), 500

@room_bp.route('/update_status/<int:room_id>', methods=['PUT'])
def update_status(room_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({'error': 'Missing status field'}), 400

    # Rechercher la chambre par ID
    room = Room.query.get(room_id)

    if not room:
        return jsonify({'error': 'Room not found'}), 404

    # Mettre à jour le statut de la chambre
    room.status = new_status
    db.session.commit()

    return jsonify({'message': 'Room status updated successfully', 'room_id': room_id, 'new_status': new_status}), 200

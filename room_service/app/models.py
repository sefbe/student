from app import db

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='disponible')  # Ajout de l'attribut status

    # Relation avec les images (relation One-to-Many)
    images = db.relationship('Image', backref='room', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Room {self.title}>"

    # Méthode pour convertir l'objet Room en dictionnaire
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "location": self.location,
            "distance": self.distance,
            "owner_id": self.owner_id,
            "status": self.status,  # Inclure le status dans le résultat
            "images": [image.to_dict() for image in self.images]  # Inclure les images dans le résultat
        }

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)  # Lien avec la chambre
    image_data = db.Column(db.LargeBinary, nullable=False)  # Contenu binaire de l'image
    image_name = db.Column(db.String(255), nullable=False)  # Nom de fichier de l'image

    def __repr__(self):
        return f"<Image {self.image_name}>"

    # Méthode pour convertir l'objet Image en dictionnaire
    def to_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "image_name": self.image_name,
            "image_data": None  # Optionnel : exclure les données binaires ou utiliser Base64 pour encoder
        }

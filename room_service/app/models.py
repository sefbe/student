from app import db

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    images = db.Column(db.Text, nullable=True)  # Liste des images séparées par des virgules
    owner_id = db.Column(db.Integer, nullable=False)

    # Représentation en chaîne de caractères de l'objet
    def __repr__(self):
        return f"<Room {self.title} (Owner ID: {self.owner_id})>"

    # Méthode pour convertir l'objet en dictionnaire, utile pour les API
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "location": self.location,
            "distance": self.distance,
            "images": self.images.split(',') if self.images else []  # Transformation des images en liste
        }
    
    # Méthode pour ajouter une image à la liste d'images
    def add_image(self, image_path):
        if self.images:
            self.images += ',' + image_path
        else:
            self.images = image_path

    # Méthode pour supprimer une image de la liste d'images
    def remove_image(self, image_path):
        if self.images:
            images_list = self.images.split(',')
            if image_path in images_list:
                images_list.remove(image_path)
                self.images = ','.join(images_list)


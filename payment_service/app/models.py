from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    payer_id = db.Column(db.Integer, nullable=False)  # ID de celui qui effectue le paiement
    room_id = db.Column(db.Integer, nullable=False)   # ID de la chambre concernée
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)  # Date du paiement

    def __init__(self, payer_id, room_id):
        self.payer_id = payer_id
        self.room_id = room_id

    def to_dict(self):
        return {
            'id': self.id,
            'payer_id': self.payer_id,
            'room_id': self.room_id,
            'payment_date': self.payment_date.strftime('%Y-%m-%d %H:%M:%S')
        }


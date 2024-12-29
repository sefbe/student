from datetime import datetime, timedelta
from app import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum("proprietaire", "locataire"), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)  # Ajouter is_active ici
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    suspension_end = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def suspend(self, period_days):
        self.suspension_end = datetime.utcnow() + timedelta(days=period_days)
        db.session.commit()

    def restore(self):
        self.is_deleted = False
        self.suspension_end = None
        db.session.commit()

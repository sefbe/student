import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'room311937Sefa@')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://sef:373040Sefa%40@mysql-container/rooms_db'
    )  # Remplacez `username`, `password`, et `rooms_db` par vos informations MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'


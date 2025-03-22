import os

class Config:
    # Clé secrète pour les sessions et les flashs
    SECRET_KEY = "user311937Sefa@"
    
    # URL de la base de données MySQL avec PyMySQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://sef:373040Sefa%40@mysql-container/payment_db"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    SECRET_KEY = "user311937Sefa@"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://sef:373040Sefa%40@mysql-container/user_service_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

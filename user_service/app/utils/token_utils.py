import jwt
import datetime
from flask import current_app

def generate_token(user_id):
    """ Génére un token JWT valide pour l'utilisateur donné """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """ Vérifie un token JWT """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token expiré
    except jwt.InvalidTokenError:
        return None  # Token invalide


from datetime import datetime, timedelta,timezone
import jwt

from config import config

def generate_jwt_token(user_id, user_name):
    expires = datetime.now(timezone.utc) + timedelta(days=15)
    encode = {'user_name': user_name, "user_id": user_id, "exp": expires}
    token = jwt.encode(encode, config.SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
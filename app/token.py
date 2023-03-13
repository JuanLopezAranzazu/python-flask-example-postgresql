import os
from datetime import datetime, timedelta
from jose import jwt
from functools import wraps
from flask import request, jsonify
from . import models

SECRET_KEY = os.getenv("secret_key")
ALGORITHM = os.getenv("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("access_token_expire_minutes"))


def create_access_token(data):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
  
  
def verify_access_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token no encontrado!'}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(*args, **kwargs)

    return decorator


def get_current_user():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split()[1]

    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        user = models.User.query.get(id)
        return user
    except:
        return None
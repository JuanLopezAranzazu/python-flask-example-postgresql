from flask import jsonify, request
from ..main import app, db
from .. import models, schemas
from passlib.context import CryptContext

from ..token import create_access_token, verify_access_token, get_current_user

# api de autenticacion
# http://127.0.0.1:5000/authentication/

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


prefix = "/authentication"


@app.route(f"{prefix}/login/", methods=['POST'])
def login():
  email = request.json['email']
  password = request.json['password']
  
  user = models.User.query.filter_by(email=email).first()
  
  if not user:
        return jsonify({"message": "Invalid Credentials"}), 403

  if not pwd_context.verify(password, user.password):
        return jsonify({"message": "Invalid Credentials"}), 403
  
  access_token = create_access_token(data={"user_id": user.id})
  
  return jsonify({"access_token": access_token, "token_type": "bearer"})


@app.route(f"{prefix}/protected/")
@verify_access_token
def protected():
  return jsonify({'message': 'Acceso permitido!'})


@app.route(f"{prefix}/current_user")
def current_user():
  user = get_current_user()
  
  if not user:
    return jsonify({"message": "Token inválido o caducado"}), 401

  return schemas.user_schema.jsonify(user)

  
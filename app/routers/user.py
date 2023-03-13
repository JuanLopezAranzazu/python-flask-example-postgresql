from flask import jsonify, request
from ..main import app, db
from .. import models, schemas
from passlib.context import CryptContext

# api de usuarios
# http://127.0.0.1:5000/users/

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


prefix = "/users"

@app.route(f"{prefix}/")
def get_users():
  users = models.User.query.all()
  return jsonify(schemas.users_schema.dump(users))


@app.route(f"{prefix}/<id>")
def get_user(id):
  user = models.User.query.get(id)
  
  if not user:
        return jsonify({"message": "User not found"}), 404
  
  return schemas.user_schema.jsonify(user)


@app.route(f"{prefix}/", methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    
    hashed_password = pwd_context.hash(password)

    user = models.User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User already exists"}), 400

    new_user = models.User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return schemas.user_schema.jsonify(new_user), 201


@app.route(f"{prefix}/<id>", methods=['PUT'])
def update_user(id):
    user = models.User.query.get(id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    email = request.json['email']
    password = request.json['password']
    
    hashed_password = pwd_context.hash(password)

    user.email = email
    user.password = hashed_password

    db.session.commit()

    return schemas.user_schema.jsonify(user)


@app.route(f"{prefix}/<id>", methods=['DELETE'])
def delete_user(id):
    user = models.User.query.get(id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
      
    db.session.delete(user)
    db.session.commit()
    
    return "", 204


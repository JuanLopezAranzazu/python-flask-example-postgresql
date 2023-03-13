import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

load_dotenv()

app = Flask(__name__)

database_hostname = os.getenv("database_hostname")
database_port = os.getenv("database_port")
database_password = os.getenv("database_password")
database_name = os.getenv("database_name")
database_username = os.getenv("database_username")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}"

db = SQLAlchemy(app)
ma = Marshmallow(db)

from . import models, schemas


with app.app_context():
    db.create_all()
    # new_user = models.User(email="example@gmail.com",password="example")
    # db.session.add(new_user)
    # db.session.commit()


# flask --app main run --debug
# http://127.0.0.1:5000/

@app.route("/")
def root():
  return jsonify({ "message": "Hola mundo" })


@app.route("/template/")
def template():
  users = models.User.query.all()
  return render_template("base.html", list_user=users)

# routers
from .routers import user, auth


if __name__ == "__main__":
  app.run(debug=True)


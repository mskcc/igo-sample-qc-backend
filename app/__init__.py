# app/__init__.py


from flask import Flask, json, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_jwt_extended import (
    JWTManager)

app = Flask(__name__)



app.config.from_pyfile("../secret_config.py")

db = SQLAlchemy(app)
jwt = JWTManager(app)


from app.models import Comment
# added by anna
# from app.models import User

db.create_all()


from .views.comment import comment
app.register_blueprint(comment)

# added by anna
from .views.user import user
app.register_blueprint(user)


CORS(app)


@app.route("/checkVersion")
def index():
    return "Welcome to Sample QC Reporting"

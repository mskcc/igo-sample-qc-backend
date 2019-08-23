# app/__init__.py


from flask import Flask, json, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.from_pyfile("../secret_config.py")

db = SQLAlchemy(app)


from app.models import Comment

db.create_all()


from .views.comment import comment
app.register_blueprint(comment)


CORS(app)


@app.route("/checkVersion")
def index():
    return "Welcome to Sample QC Reporting"

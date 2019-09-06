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

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return BlacklistToken.is_jti_blacklisted(jti)


from app.models import Comment, BlacklistToken, User


db.create_all()


from .views.comment import comment
app.register_blueprint(comment)

from .views.user import user
app.register_blueprint(user)

from .views.qcresult import qcresult
app.register_blueprint(qcresult)

from .views.tree import tree
app.register_blueprint(tree)


CORS(app)


@app.route("/checkVersion")
def index():
    return "Welcome to Sample QC Reporting"

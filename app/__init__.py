# app/__init__.py


from flask import Flask, json, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_jwt_extended import JWTManager
import flask_login
import logging

from logging.config import dictConfig


dictConfig(
    {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(message)s'
                # 'format': '[%(asctime)s] SAMPLE.REC.BE %(levelname)s in %(module)s: %(message)s'
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            }
        },
        'root': {'level': 'INFO', 'handlers': ['wsgi']},
    }
)


app = Flask(__name__)


app.config.from_pyfile("../secret_config.py")

db = SQLAlchemy(app)
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return BlacklistToken.is_jti_blacklisted(jti)


login_manager = flask_login.LoginManager()

login_manager.init_app(app)

from app.models import BlacklistToken, Comment, CommentRelation, Decision, User


db.create_all()


from .views.comment import comment

app.register_blueprint(comment)

from .views.user import user

app.register_blueprint(user)

from .views.qc_report import qc_report

app.register_blueprint(qc_report)

from .views.tree import tree

app.register_blueprint(tree)


CORS(app)


@app.route("/checkVersion")
def index():
    return "Welcome to Sample QC Reporting"
# app/__init__.py


from flask import Flask, json, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_jwt_extended import JWTManager, get_jwt_identity
import flask_login


app = Flask(__name__)


app.config.from_pyfile("../secret_config.py")

# LOGGING
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


import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ENV = app.config["ENV"]
# if ENV == "development":
#     logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


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


from app.logger import log_info, log_error, log_lims


@app.route("/checkVersion")
def index():
    return "Welcome to Sample QC Reporting"


@app.after_request
def after_request(response):
    # response.headers.add("Access-Control-Allow-Origin", "*")
    response_message = ""
    if request.method != "OPTIONS":

        # print(response.headers)
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
        request_args = {key + ":" + request.args[key] for key in request.args}

        if response.is_streamed == True:
            response_message = (
                "\n---Flask Request---\n"
                + ",".join(request_args)
                + "\n"
                + "Streamed Data"
                + "\n"
            )

        elif request.path == "/addAndNotify" or request.path == "/addAndNotifyInitial":
            return response
        elif request.path == "/login":
            response_message = ""

        elif request.path == "/getAttachmentFile":
            response_message = (
                "Args: "
                + ",".join(request_args)
                + "Data: File Data"
                + "\n"
                + "User: "
                + str(get_jwt_identity())
                + "\n"
            )

        else:
            if len(response.data) > 500:
                data = str(response.data[:500]) + "[...]"
            else:
                data = str(response.data)

            if request.method == "GET":

                response_message = (
                    "USER: "
                    + str(get_jwt_identity())
                    + "\n"
                    + 'GET ARGS: '
                    + ",".join(request_args)
                    + "\n"
                    + "RESPONSE DATA: "
                    + str(data)
                )
            elif request.method == "POST":
                post = str(request.get_json()["data"])
                if len(post) > 500:
                    post = post[:500] + "[...]"

                response_message = (
                    "USER: "
                    + str(get_jwt_identity())
                    + "\n"
                    + 'POST DATA: '
                    + str(post)
                    + "\n"
                    + "RESPONSE DATA: "
                    + str(data)
                )

            else:
                response_message = (
                    "USER: "
                    + str(get_jwt_identity())
                    + "\n"
                    + 'METHOD: '
                    + request.method
                    + "\n"
                    + "RESPONSE DATA: "
                    + str(data)
                )
        log_info(response_message)
    return response

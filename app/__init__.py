# app/__init__.py

from flask import Flask, request
from datetime import datetime
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile("../secret_config.py")

db = SQLAlchemy(app)


from app.models import Comment

db.create_all()

# db.session.commit()


# @app.route("/")
# def index():
#     return "Welcome to Sample QC Reporting"
CORS(app)

@app.route("/getComments")
def comment():
    # payload = request.get_json()['data']
    # print(payload)
    # form_values = payload['form_values']
    # submissions = Submission.query.filter(Submission.username == username).all()

    comments = Comment.query.all()
    comments_response = []
    for comment in comments:
        comments_response.append(comment.serialize)
        # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    return json.dumps(comments_response)


@app.route("/addComment", methods=['POST'])
def save_comment():
    # some json
    payload = '{"username": "duniganm","user_title": "project manager","comment": "qc is ready","request_id": "06304_B","qc_table": "dna"}'

    # payload = request.get_json()['data']
    # print(payload)
    # form_values = payload['form_values']
    # submissions = Submission.query.filter(Submission.username == username).all()

    # parse payload
    pycomment = json.loads(payload)
    # pycomment = payload

    # python dictionary is saved to db
    comment = Comment(
        username=pycomment["username"],
        user_title=pycomment["user_title"],
        comment=pycomment["comment"],
        request_id=pycomment["request_id"],
        qc_table=pycomment["qc_table"],
        date_created=datetime.now(),
        date_updated=datetime.now(),
    )
    db.session.add(comment)
    db.session.commit()

    comments = Comment.query.all()
    comments_response = []
    for x in comments:
        comments_response.append(x.serialize)
        # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))

    return json.dumps(comments_response)
    responseObject = {'comments': comments}

    return make_response(jsonify(responseObject), 200, None)


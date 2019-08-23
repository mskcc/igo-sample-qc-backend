from flask import Flask, Blueprint, json, jsonify, request, make_response
from app import db
from app.models import Comment

from datetime import datetime

# initialize comment blueprint as an extension of the application
comment = Blueprint('comment', __name__)


# change to accept a request argument, request_id, and only return applicable comments
@comment.route("/getComments")
# @app.route("/getComments", methods=['GET'])
def get_comments():
    # TO CHANGE
    # submission = Submission.query.filter(
    #     Submission.username == request.args.get("username"),
    #     Submission.service_id == request.args.get("service_id"),
    # ).first()

    comments = Comment.query.all()
    comments_response = []
    for comment in comments:
        comments_response.append(comment.serialize)
        # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)


@comment.route("/addComment")
# @app.route("/addComment", methods=['POST'])
# change to accept a request payload, the new comment, save it to the DB and only return comments with the same request id
def save_comment():
    # some json
    payload = '{"username": "duniganm","user_title": "project manager","comment": "qc is ready","request_id": "06304_B","qc_table": "dna"}'

    # TO CHANGE
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

    responseObject = {'comments': comments_response}

    return make_response(jsonify(responseObject), 200, None)

from flask import Flask, Blueprint, json, jsonify, request, make_response
from app import db
from app.models import Comment

from datetime import datetime

# initializes comment blueprint as an extension of the application
comment = Blueprint('comment', __name__)


# accepts a request argument, request_id, and returns applicable comments
@comment.route("/getComments", methods=['GET'])
def get_comments():

    comments_response = load_comments_for_request()
    # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)

# accepts a request payload, the new comment, saves it to the DB, and returns comments with the same request_id
@comment.route("/addComment", methods=['POST'])
def save_comment():
    
    # accepts a request payload and converts it to json
    payload = request.get_json()['data']
    # print(payload)

    # parses python dictionary into table's fields
    comment = Comment(
        username=payload["username"],
        user_title=payload["user_title"],
        comment=payload["comment"],
        request_id=payload["request_id"],
        qc_table=payload["qc_table"],
        date_created=datetime.now(),
        date_updated=datetime.now(),
    )
    # adds and commits changes to db
    db.session.add(comment)
    db.session.commit()

    # returns comments for a specific request
    comments_response = load_comments_for_request()
    # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))

    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)


# -------- UTIL --------


# goes to Comment model/table and grabs everything in it
def load_comments():
    comments = Comment.query.all()
    comments_response = []
    for x in comments:
        comments_response.append(x.serialize)
    return comments_response


# goes to Comment model/table and grabs comments for a specific request
def load_comments_for_request():
    comments = Comment.query.filter(
        Comment.request_id == request.args.get("request_id"))
    comments_response = []
    for x in comments:
        comments_response.append(x.serialize)
    return comments_response
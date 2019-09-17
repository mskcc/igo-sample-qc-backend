from flask import Flask, Blueprint, json, jsonify, request, make_response
from app import db
from app.models import Comment
from sqlalchemy import update

from datetime import datetime

# initializes comment blueprint as an extension of the application
comment = Blueprint('comment', __name__)


# accepts a request argument, request_id, and returns applicable comments
@comment.route("/getComments", methods=['GET'])
def get_comments():

    request_id = request.args.get("request_id")
    # check if there are comments for that request
    comments_response = load_comments_for_request(request_id)
    # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    # if there are no comments for the request
    if not comments_response:
        return make_response('no comments', 200, None)
    # there are comments for the request
    else:
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


# accepts comment_id, new content and updates the comment with new content
# test using http://localhost:5000/editComment?id=3&content=%22new%20content%22
@comment.route("/editComment", methods=['GET'])
def edit_comment():
    
    # get the id of the comment
    comment_id = request.args.get("id")
    responseObject = {'id': comment_id}
    
    # get the new comment content
    new_content = request.args.get("content")
    
    # update comment where the comment_id is equal to id in Comment table
    comment = Comment.query.filter(
        Comment.id == comment_id).first()
    comment.comment = new_content
    db.session.commit()

    return make_response(jsonify(responseObject), 200, None)

# accepts comment_id and deletes row
@comment.route("/deleteComment", methods=['GET'])
def delete_comment():

    # get the id of the comment
    comment_id = request.args.get("id")
    responseObject = {'id': comment_id}
    
    # delete comment where the comment_id is equal to id in Comment table
    comment = Comment.query.filter(
        Comment.id == comment_id).first()
    db.session.delete(comment)
    db.session.commit()

    return make_response(jsonify(responseObject), 200, None)



# -------- UTIL --------


# goes to Comment model/table and grabs everything in it
def load_comments():
    comments = Comment.query.all()
    comments_response = []
    for x in comments:
        comments_response.append(x.serialize)
    return comments_response


# goes to Comment model/table and grabs comments for a specific request_id
def load_comments_for_request(request_id):
    comments = Comment.query.filter(
        Comment.request_id == request_id)
    comments_response = []
    for x in comments:
        comments_response.append(x.serialize)
    return comments_response
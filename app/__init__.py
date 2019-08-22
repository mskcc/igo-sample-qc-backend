# app/__init__.py

from flask import Flask
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
    comments = Comment.query.all()
    comments_response = []
    for comment in comments:
        comments_response.append(comment.serialize)
        # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    return json.dumps(comments_response)


# /addComment
# https://www.w3schools.com/python/python_json.asp
# accepts a new comment like
# {"username": "patrunoa", "user_title": "app analyst", "comment": "qc is ready", "request_id": "06304", "qc_table": "dna"}
# insert/save it to the database
# return all comments

# @app.route('/saveSubmission', methods=['POST'])
# def save_submission():

# json - > python dictionary
#     payload = {"username": "patrunoa", "user_title": "app analyst", "comment": "qc is ready", "request_id": "06304", "qc_table": "dna"}

#     # save version in case of later edits that aren't compatible anymore
#     submission = Submission(
#         username=username,
#         service_id=form_values['service_id'],
#         transaction_id=None,
#         material=form_values['material'],
#         application=form_values['application'],
#         form_values=json.dumps(form_values),
#         grid_values=json.dumps(grid_values),
#         version=VERSION,
#     )
        # db.session.add(submission)
        # db.session.commit()

#     responseObject = {
#         'comments': comments,
#     }

#     return make_response(jsonify(responseObject), 200, None)



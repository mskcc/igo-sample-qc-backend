# app/__init__.py

from flask import Flask
import json
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


@app.route("/")
def comment():
    comments = Comment.query.all()
    comments_response = []
    for comment in comments:
        comments_response.append(comment.serialize)
        # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    return json.dumps(comments_response)

    # submissions = Submission.query.filter(Submission.username == username).all()

    # submissions_response = []
    # for submission in submissions:
    # submissions_response.append(submission.serialize)
    #     # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    # return submissions_response

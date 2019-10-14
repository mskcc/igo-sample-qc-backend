from flask import Flask, Blueprint, json, jsonify, request, make_response
from app import db
from app.models import Comment, CommentRelation
from sqlalchemy import update

# Import smtplib for the actual sending function
import smtplib
from email.mime.text import MIMEText

# Import the email modules we'll need
from email.message import EmailMessage
from datetime import datetime

# initializes comment blueprint as an extension of the application
comment = Blueprint('comment', __name__)


# accepts a request argument, request_id, and returns applicable comments
@comment.route("/getComments", methods=['GET'])
def get_comments():

    # payload = request.get_json()['data']
    # print(payload)
    # request_id = payload["request_id"]
    request_id = request.args.get("request_id")
    # check if there are comments for that request
    comments_response = load_comments_for_request(request_id)
    # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    # if there are no comments for the request
    # if not comments_response:
    #     return make_response('no comments', 200, None)
    # # there are comments for the request
    # else:
    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)


# accepts a request payload, the new comment, saves it to the DB, and returns comments with the same request_id
@comment.route("/addAndNotifyInitial", methods=['POST'])
def addAndNotifyInitial():
    payload = request.get_json()['data']

    try:
        save_initial_comment_and_relation(
            payload["comment"],
            payload["reports"],
            payload["recipients"],
            payload["request_id"],
        )
    except:
        responseObject = {'message': "Failed to save comment"}

        return make_response(jsonify(responseObject), 401, None)

    # returns comments for a specific request
    comments_response = load_comments_for_request(payload["request_id"])

    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)

@comment.route("/addAndNotify", methods=['POST'])
def addAndNotify():
    payload = request.get_json()['data']

    try:
        save_comment_and_relation(
            payload["comment"],
            payload["reports"],
            payload["request_id"],
        )
    except:
        responseObject = {'message': "Failed to save comment"}

        return make_response(jsonify(responseObject), 400, None)

    # returns comments for a specific request
    comments_response = load_comments_for_request(payload["request_id"])

    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)


# SENDMAIL = "/usr/sbin/sendmail"  # sendmail location

# @qc_report.route("/notifyInitial", methods=["POST"])
# def notifyInitial():
#     # p = os.popen("%s -t" % SENDMAIL, "w")
#     # p.write("To: wagnerl@mskcc.org\n")
#     # p.write("From: igoski@mskcc.org\n")
#     # p.write("Subject: test\n")
#     # p.write("\n") # blank line separating headers from body
#     # p.write("Some text\n")
#     # p.write("some more text\n")
#     # sts = p.close()

#     # def notify(self, runType, delivered, text, mainContacts, additionalContacts):
#     #     subjectType = runType
#     #     if subjectType == "WESAnalysis":
#     #         subjectType = delivered.requestType
#     #     msg = MIMEText(text)
#     #     msg['Subject'] = "Delivery: " + delivered.userName + " sequencing data - " + subjectType + " project " + delivered.requestId
#     #     msg['From'] = SENDER_ADDRESS
#     #     msg['To'] = ",".join(mainContacts)
#     #     msg['Cc'] = ",".join(additionalContacts)
#     #     s = smtplib.SMTP('localhost')
#     #     s.sendmail(SENDER_ADDRESS, mainContacts + additionalContacts, msg.as_string())
#     #     s.close()
#     # msg = EmailMessage()
#     # msg.set_content('testtesttest')

#     # me == the sender's email address
#     # you == the recipient's email address
#     msg = MIMEText("testtesttest")
#     msg['Subject'] = 'Sample QC Test'
#     msg['From'] = "wagnerl@mskcc.org"
#     msg['To'] = "wagnerl@mskcc.org"
#     # # msg['Cc'] = "wagnerl@mskcc.org"

#     # # # Send the message via our own SMTP server.
#     s = smtplib.SMTP('localhost')
#     s.sendmail("wagnerl@mskcc.org", "wagnerl@mskcc.org", msg.as_string())
#     s.close()


@comment.route("/addComment", methods=['POST'])
def save_comment():

    # accepts a request payload and converts it to json
    payload = request.get_json()['data']
    # save_initial_comment(payload)
    # def save_initial_comment(comment, reports, recipients, request_id):
    try:
        save_initial_comment(
            payload["comment"],
            payload["report"],
            payload["recipients"],
            payload["request_id"],
        )
    except:
        responseObject = {'message': "Failed to save comment"}

        return make_response(jsonify(responseObject), 401, None)

    # returns comments for a specific request
    comments_response = load_comments_for_request(payload["request_id"])
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
    comment = Comment.query.filter(Comment.id == comment_id).first()
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
    comment = Comment.query.filter(Comment.id == comment_id).first()
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
    comment_relations = CommentRelation.query.filter(
        CommentRelation.request_id == request_id
    )
    # comments = Comment.query.filter(Comment.commentrelation_id == comment_relation.id).all()
    if not (comment_relations):
        return None
    else:
        comments_response = {
                "DNA Report": {"comments":[], "recipients":[]},
                "RNA Report": {"comments":[], "recipients":[]},
                "Library Report": {"comments":[], "recipients":[]},
                "Pathology Report": {"comments":[], "recipients":[]},
            }
        
        for comment_relation in comment_relations:
            print(comment_relation.reports)
            comments = comment_relation.children
            reports = comment_relation.reports
            comments_response[comment_relation.reports]["recipients"].append(comment_relation.recipients)
           
            for comment in comments:
                # if comment belongs to mutl reports, attach to every one in response
                if ',' in comment_relation.reports:
                    reports = comment_relation.reports.split(",")
                    for report in reports:
                        comments_response[report]["comments"].append(comment.serialize)
                       
                else:
                    comments_response[comment_relation.reports]["comments"].append(comment.serialize)
                  

    # delete reports without comments from response object
    reports_without_comments = {
        k: v for k, v in comments_response.items() if len(v["comments"]) == 0
    }

    for to_delete in reports_without_comments:
        if to_delete in comments_response:
            del comments_response[to_delete]
    return comments_response


def save_initial_comment_and_relation(comment, reports, recipients, request_id):
    comment_relation = (
        CommentRelation.query.filter(CommentRelation.request_id == request_id)
        .filter(CommentRelation.reports == reports)
        .filter(CommentRelation.recipients == recipients)
        .first()
    )
    if not (comment_relation):
        comment_relation = CommentRelation(
            request_id=request_id,
            reports=reports,
            recipients=recipients,
            date_created=datetime.now(),
            date_updated=datetime.now(),
        )
        db.session.add(comment_relation)
    print(comment)
    comment = Comment(
        username=comment["username"],
        user_title="test",
        comment=comment["content"],
        date_created=datetime.now(),
        date_updated=datetime.now(),
    )
    comment_relation.children.append(comment)
    db.session.commit()

    return

def save_comment_and_relation(comment, reports, request_id):
    comment_relation = (
        CommentRelation.query.filter(CommentRelation.request_id == request_id)
        .filter(CommentRelation.reports == reports)
        .first()
    )
    if not (comment_relation):
        comment_relation = CommentRelation(
            request_id=request_id,
            reports=reports,
            recipients=recipients,
            date_created=datetime.now(),
            date_updated=datetime.now(),
        )
        db.session.add(comment_relation)
    print(comment)
    comment = Comment(
        username=comment["username"],
        user_title="test",
        comment=comment["content"],
        date_created=datetime.now(),
        date_updated=datetime.now(),
    )
    comment_relation.children.append(comment)
    db.session.commit()

    return


def save_comment(payload):
    print(payload)

    comment = Comment(
        username=payload["username"],
        user_title="test",
        comment=payload["comment"],
        request_id=payload["request_id"],
        date_created=datetime.now(),
        date_updated=datetime.now(),
    )
    # adds and commits changes to db
    db.session.add(comment)
    db.session.commit()
    return

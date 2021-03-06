from flask import Flask, Blueprint, json, jsonify, request, make_response
from app import app, db, constants, notify
from app.models import Comment, CommentRelation, User, Decision
from sqlalchemy import update, text

import traceback

from app.logger import log_info, log_error
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
)

import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from datetime import datetime

NOTIFICATION_SENDER = app.config["NOTIFICATION_SENDER"]
IGO_EMAIL = app.config["IGO_EMAIL"]
ENV = app.config["ENV"]
# initializes comment blueprint as an extension of the application
comment = Blueprint('comment', __name__)


# accepts a request argument, request_id, and returns applicable comments
@comment.route("/getComments", methods=['GET'])
@jwt_required
def get_comments():
    request_id = request.args.get("request_id")
    comments_response = load_comments_for_request(request_id)
    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)


# accepts a request payload, the new comment, saves it to the DB, and returns comments with the same request_id
@comment.route("/addAndNotifyInitial", methods=['POST'])
@jwt_required
def add_and_notify_initial():
    payload = request.get_json()['data']

    try:
        recipients = ""
        user = User.query.filter_by(username=payload["comment"]["username"]).first()
        for report in payload["reports"]:
            comment_relation = save_initial_comment_and_relation(
                payload["comment"],
                report,
                payload["recipients"],
                payload["request_id"],
                payload["decisions_made"],
                payload["is_cmo_pm_project"],
                # add decisionsmade object
                user,
            )
            is_cmo_pm_project = payload["is_cmo_pm_project"]
            is_pathology_report = report == "Pathology Report"
            is_covid_report = report == "COVID19 Report"
            if comment_relation:
                if (
                    comment_relation.decision
                    and comment_relation.decision[0].is_igo_decision
                ) or is_covid_report :
                    is_decided = True
                else:
                    is_decided = False
                notify.send_initial_notification(
                    set(comment_relation.recipients.split(',')), payload["request_id"], report, user, is_decided, is_pathology_report,is_covid_report, is_cmo_pm_project
                )
            else:
                responseObject = {'message': "Failed to save comment"}
                return make_response(jsonify(responseObject), 400, None)

    except:
        traceback.print_exc()

        responseObject = {'message': "Failed to save comment"}

        return make_response(jsonify(responseObject), 400, None)

    # returns comments for a specific request
    comments_response = load_comments_for_request(payload["request_id"])

    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)


@comment.route("/addAndNotify", methods=['POST'])
@jwt_required
def add_and_notify():
    payload = request.get_json()['data']
    try:

        user = User.query.filter_by(username=payload["comment"]["username"]).first()
        comment_relation = (
            CommentRelation.query.filter(
                CommentRelation.request_id == payload["request_id"]
            )
            .filter(CommentRelation.report == payload["report"])
            .first()
        )
        recipients = save_comment(
            payload["comment"],
            payload["report"],
            payload["request_id"],
            user,
            comment_relation,
        )

        # print(recipients)
        # if saving worked
        if recipients:
            if user.role == "lab_member":
                recipients = (
                    recipients + "," + payload["comment"]["username"] + "@mskcc.org"
                )
                recipients = recipients.split(",")
                recipients = set(recipients)
                notify.send_notification(
                    recipients,
                    payload["comment"],
                    payload["request_id"],
                    payload["report"],
                    user,
                )
            else:
                # if a non-lab member comments, notify intial comments author
                recipients = recipients + "," + comment_relation.author + "@mskcc.org"
                recipients = recipients.split(",")
                notify.send_notification(
                    set(recipients),
                    payload["comment"],
                    payload["request_id"],
                    payload["report"],
                    user,
                )

    except:
        print(traceback.print_exc())
        responseObject = {'message': "Failed to save comment"}

        return make_response(jsonify(responseObject), 400, None)

    # returns comments for a specific request
    comments_response = load_comments_for_request(payload["request_id"])

    responseObject = {'comments': comments_response}
    return make_response(jsonify(responseObject), 200, None)


@comment.route("/addToAllAndNotify", methods=['POST'])
@jwt_required
def add_to_all_and_notify():
    payload = request.get_json()['data']
    try:
        recipients = []
        user = User.query.filter_by(username=payload["comment"]["username"]).first()

        for report in payload["reports"]:
            comment_relation = (
                CommentRelation.query.filter(
                    CommentRelation.request_id == payload["request_id"]
                )
                .filter(CommentRelation.report == report)
                .first()
            )
            recipients = save_comment(
                payload["comment"],
                report,
                payload["request_id"],
                user,
                comment_relation,
            )
            if recipients:
                if user.role == "lab_member":
                    recipients = recipients.split(",")
                    notify.send_notification(
                        set(recipients),
                        payload["comment"],
                        payload["request_id"],
                        report,
                        user,
                    )
                else:
                    # if a non-lab member comments, notify intial comments author
                    recipients = (
                        recipients + "," + comment_relation.author + "@mskcc.org"
                    )
                    recipients = recipients.split(",")
                    notify.send_notification(
                        set(recipients),
                        payload["comment"],
                        payload["request_id"],
                        report,
                        user,
                    )
    except:
        print(traceback.print_exc())
        responseObject = {'message': "Failed to save comment"}

        return make_response(jsonify(responseObject), 400, None)

    # returns comments for a specific request
    comments_response = load_comments_for_request(payload["request_id"])

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
    if len(comments) > 0:
        for x in comments:
            comments_response.append(x.serialize)
    else:
        print("NO COMMENT FOUND")
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
            "DNA Report": {"comments": [], "recipients": ""},
            "RNA Report": {"comments": [], "recipients": ""},
            "Pool Report": {"comments": [], "recipients": ""},
            "Library Report": {"comments": [], "recipients": ""},
            "Pathology Report": {"comments": [], "recipients": ""},
            "COVID19 Report": {"comments": [], "recipients": ""},
        }

        for comment_relation in comment_relations:
            comments_response[comment_relation.report][
                "recipients"
            ] = comment_relation.recipients
            comments = comment_relation.children
            report = comment_relation.report

            for comment in comments:
                user = User.query.filter_by(username=comment.username).first()
                comment_dict = comment.serialize
                user_dict = user.serialize
                comment_dict.update(user_dict)
                comments_response[report]["comments"].append(comment_dict)

    # delete reports without comments from response object
    reports_without_comments = {
        k: v for k, v in comments_response.items() if len(v["comments"]) == 0
    }

    for to_delete in reports_without_comments:
        if to_delete in comments_response:
            del comments_response[to_delete]
    return comments_response


#  saves initial new comment and relation and returns recipients to send notification to
def save_initial_comment_and_relation(
    comment, report, recipients, request_id, decisions_made, is_cmo_pm_project, user
):  
    comment_relation = (
        CommentRelation.query.filter(CommentRelation.request_id == request_id)
        .filter(CommentRelation.report == report)
        .filter(CommentRelation.recipients == recipients)
        .first()
    )

    if not (comment_relation):
        comment_relation = CommentRelation(
            request_id=request_id,
            report=report,
            recipients=recipients,
            is_cmo_pm_project= is_cmo_pm_project,
            date_created=datetime.now(),
            date_updated=datetime.now(),
        )
        # print(comment_relation.serialize)
        db.session.add(comment_relation)
    # print(comment)

    comment = Comment(
        comment=comment["content"],
        date_created=datetime.now(),
        date_updated=datetime.now(),
    )
    try:
        user.comments.append(comment)
        user.commentrelations.append(comment_relation)
        comment_relation.children.append(comment)

        # an inital comment was submitted for a report where all decisions have been made in the LIMS already
        if report in decisions_made:
            # create new decision
            decision = Decision(
                decisions=json.dumps(decisions_made[report]),
                request_id=request_id,
                report=report,
                is_igo_decision=True,
                is_submitted=True,
                date_created=datetime.now(),
                date_updated=datetime.now(),
            )
            user.decisions.append(decision)
            comment_relation.decision.append(decision)

        db.session.commit()
    except:
        print(traceback.print_exc())
        return None

    return comment_relation


#  saves new comment and returns recipients to send notification to
def save_comment(comment, report, request_id, user, comment_relation):
    comment_to_save = Comment(
        comment=comment["content"],
        date_created=datetime.now(),
        date_updated=datetime.now(),
    )
    # comments that already have a exact relation:

    try:
        comment_relation.children.append(comment_to_save)
        user.comments.append(comment_to_save)
        db.session.commit()
        return comment_relation.recipients
    except:
        print(traceback.print_exc())

        return None

    return

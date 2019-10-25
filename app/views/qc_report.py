from flask import (
    Flask,
    Blueprint,
    json,
    jsonify,
    request,
    make_response,
    send_from_directory,
    send_file,
)
import requests
from datetime import datetime
import os.path
import uwsgi, pickle
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
import pandas as pd
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from datetime import datetime

from openpyxl.writer.excel import save_virtual_workbook

import sys
import re
import copy
import traceback

from app import app, constants, db
from app.models import Comment, CommentRelation, Decision, User

# MORE IMPORTANT THAN IT SHOULD BE
app.config['JSON_SORT_KEYS'] = False
# _________________________________

LIMS_API_ROOT = app.config["LIMS_API_ROOT"]
LIMS_USER = app.config["LIMS_USER"]
LIMS_PW = app.config["LIMS_PW"]
TMP_FOLDER = app.config["TMP_FOLDER"]
NOTIFICATION_SENDER = app.config["NOTIFICATION_SENDER"]
IGO_EMAIL = app.config["IGO_EMAIL"]

qc_report = Blueprint("qc_report", __name__)


s = requests.Session()

# returns request level information including a list of samples in the request
# queries IGO LIMS REST
@qc_report.route("/getRequestSamples", methods=['GET'])
def get_request_samples():
    return_text = ""

    request_id = request.args.get("request_id")
    username = request.args.get("username")
    role = request.args.get("role")
    # users see requests if they are a lab member
    # if they are associated with request AND if request already has a comment
    user_authorized_for_request = (
        role == "lab_member" or is_user_authorized_for_request(request_id, username)
    )
    # return is_dec_maker
    if user_authorized_for_request == False:
        response = make_response(
            "Request not found or not associated with your username.", 404, None
        )
        return response
    else:
        # the API endpoint
        r = s.get(
            LIMS_API_ROOT + "/api/getRequestSamples?request=" + request_id,
            auth=(LIMS_USER, LIMS_PW),
            verify=False,
        )
        if r.status_code == 200:
            return_text += r.text
            lims_data = r.json()

            responseData = {}

            if "samples" in lims_data:
                responseData["request"] = {}
                responseData["request"]["samples"] = []
                responseData["recipients"] = {}

                responseData["request"]["requestId"] = lims_data["requestId"]
                responseData["request"]["LabHeadName"] = lims_data["labHeadName"]
                responseData["request"]["investigatorName"] = lims_data[
                    "investigatorName"
                ]
                responseData["recipients"]["IGOEmail"] = "zzPDL_CMO_IGO@mskcc.org"
                responseData["recipients"]["LabHeadEmail"] = lims_data["labHeadEmail"]
                responseData["recipients"]["InvestigatorEmail"] = lims_data[
                    "investigatorEmail"
                ]
                responseData["recipients"]["OtherContactEmails"] = lims_data[
                    "otherContactEmails"
                ]

                # we only need Investigator Sample Ids
                for sample in lims_data["samples"]:
                    responseData["request"]["samples"].append(
                        sample["investigatorSampleId"]
                    )

                return make_response(responseData, r.status_code, None)
            else:
                response = make_response(
                    "Request not found or not associated with your username.", 404, None
                )
        else:

            response = make_response(r.text, r.status_code, None)
            return response

        response = make_response(return_text, 200, None)

    return response


# queries SAPIO LIMS REST
@qc_report.route("/getQcReportSamples", methods=["POST"])
def get_qc_report_samples():
    data = dict()
    payload = request.get_json()["data"]
    request_id = payload["request"]
    samples = payload["samples"]
    data['request'] = request_id
    data['samples'] = samples

    r = s.post(
        LIMS_API_ROOT + "/getQcReportSamples",
        auth=(LIMS_USER, LIMS_PW),
        verify=False,
        data=data,
    )
    # print(data)
    # dnar = s.get(
    #     LIMS_API_ROOT + "/api/getRequestSamples?request=" + request_id,
    #     auth=(LIMS_USER, LIMS_PW),
    #     verify=False,
    # )
    # print(constants.allColumns)
    return_text = ""
    if r.status_code == 200:
        # assemble table data
        lims_data = r.json()
        columnFeatures = dict()
        tables = dict()
        print(lims_data)
        for field in lims_data:

            if field == "dnaReportSamples":
                columnFeatures = mergeColumns(
                    constants.sharedColumns, constants.dnaColumns
                )
                tables[field] = build_table(
                    field, lims_data[field], columnFeatures, constants.dnaOrder
                )

            if field == "rnaReportSamples":
                columnFeatures = mergeColumns(
                    constants.sharedColumns, constants.rnaColumns
                )
                tables[field] = build_table(
                    field, lims_data[field], columnFeatures, constants.rnaOrder
                )

            if field == "libraryReportSamples":
                columnFeatures = mergeColumns(
                    constants.sharedColumns, constants.libraryColumns
                )
                tables[field] = build_table(
                    field, lims_data[field], columnFeatures, constants.libraryOrder
                )

            if field == "pathologyReportSamples":
                columnFeatures = constants.pathologyColumns
                tables[field] = build_table(
                    field, lims_data[field], columnFeatures, constants.pathologyOrder
                )

            if field == "attachments":
                columnFeatures = constants.attachmentColumns
                tables[field] = build_table(
                    field, lims_data[field], columnFeatures, constants.attachmentOrder
                )

        return make_response((jsonify(tables)), 200, None)
    else:

        response = make_response(r.text, r.status_code, None)
        return response


# r = s.get(
#        LIMS_REST_API_ROOT + "/datarecord",
#        headers=headers,
#        auth=(LIMS_API_USER, LIMS_API_PW),
#        params={
#            "datatype": "QcReportDna",
#            "field": "OtherSampleId",
#            "values": [AdCCDK_1T, AdCCDK_7T, AdCCHW],
#        },
#        verify=False,
#    )


@qc_report.route("/setQCInvestigatorDecision", methods=["POST"])
def set_qc_investigator_decision():
    payload = request.get_json()
    print(payload)
    username = payload["username"]
    decisions = payload["decisions"]
    request_id = payload["request_id"]
    try:
        decision_user = User.query.filter_by(username=username).first()

        decision_to_save = Decision(
            decisions=json.dumps(decisions),
            request_id=request_id,
            date_created=datetime.now(),
            date_updated=datetime.now(),
        )

        decision_user.decisions.append(decision_to_save)

        r = s.post(
            LIMS_API_ROOT + "/setQcInvestigatorDecision",
            auth=(LIMS_USER, LIMS_PW),
            verify=False,
            data=json.dumps(payload["decisions"]),
        )

        commentrelations = CommentRelation.query.filter_by(
            request_id=payload["request_id"]
        )
        recipients = ""
        for commentrelation in commentrelations:
            if recipients == "":
                recipients = commentrelation.recipients
            else:
                recipients = recipients + "," + commentrelation.recipients

        send_decision_notification(
            decision_to_save, decision_user, set(recipients.split(","))
        )

        db.session.commit()
        return r.text
    except:
        print(traceback.print_exc())
        db.session.rollback()

        responseObject = {'message': "Failed to submit."}
        return make_response(jsonify(responseObject), 400, None)

    # else:
    #     responseObject = {'message': "Failed to submit."}

    #     return make_response(jsonify(responseObject), 400, None)


@qc_report.route("/getPending", methods=["GET"])
def get_pending():
    # get request ids from commentrelation where not in request id from decisions
    try:
        query = db.session.query(CommentRelation)
        subquery = db.session.query(Decision.request_id)
        pendings = query.filter(~CommentRelation.request_id.in_(subquery))
        return build_pending_list(pendings)

    except:
        print(traceback.print_exc())

        return None

    # if save_decision(payload["decisions"], payload["request_id"], payload["username"]):
    #     r = s.post(
    #         LIMS_API_ROOT + "/setQcInvestigatorDecision",
    #         auth=(LIMS_USER, LIMS_PW),
    #         verify=False,
    #         data=json.dumps(payload["decisions"]),
    #     )

    #     return r.text
    # else:
    #     responseObject = {'message': "Failed to submit."}

    #     return make_response(jsonify(responseObject), 400, None)
    # return None


@qc_report.route("/downloadAttachment", methods=["GET"])
def download_attachment():

    record_id = request.args.get("recordId")
    file_name = request.args.get("fileName")

    r = s.get(
        LIMS_API_ROOT + "/getAttachmentFile",
        auth=(LIMS_USER, LIMS_PW),
        params={"recordId": record_id},
        verify=False,
    )

    if tmp_file_exists(file_name):
        log_info("Returning tmp file " + file_name)
        return send_from_directory(TMP_FOLDER, file_name, as_attachment=True)
    else:
        with open(TMP_FOLDER + file_name, 'wb') as f:
            f.write(r.content)
        log_info("Returning newly downloaded file " + file_name)
        return send_from_directory(TMP_FOLDER, file_name, as_attachment=True)


# -------------UTIL-------------
# Python code to mergeColumns dict using a single
# expression
def mergeColumns(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def build_table(reportTable, samples, columnFeatures, order):
    responseColumns = []
    responseHeaders = []
    responseSamples = []
    # print(samples)
    if not samples:
        return {}
    else:
        # sort!
        for orderedColumn in order:
            try:
                if orderedColumn in columnFeatures:

                    if "picklistName" in columnFeatures[orderedColumn]:
                        # print(responseColumns)
                        columnFeatures[orderedColumn]["source"] = get_picklist(
                            columnFeatures[orderedColumn]["picklistName"]
                        )
                        responseColumns.append(columnFeatures[orderedColumn])

                    else:
                        responseColumns.append(columnFeatures[orderedColumn])

                    if orderedColumn == "Concentration":
                        responseHeaders.append(
                            columnFeatures[orderedColumn]["columnHeader"]
                            + ' in '
                            + samples[0]['concentrationUnits']
                        )
                    else:
                        responseHeaders.append(
                            columnFeatures[orderedColumn]["columnHeader"]
                        )

            except:
                # If we didn't expect it to be returned from LIMS, delete it.
                print(
                    orderedColumn + " not found in expected columns for " + reportTable
                )
                print(traceback.print_exc())

                try:
                    # delete field from sample if we don't expect it in the FE
                    for sample in responseSamples:
                        sample.pop(orderedColumn)
                except:
                    #
                    # if sample.pop failed, excpected column not found in LIMS result, return it to FE anyway.
                    print(traceback.print_exc())
                    responseColumns[orderedColumn] = {}
                    responseHeaders.append(
                        columnFeatures[orderedColumn]["columnHeader"]
                    )

        for sample in samples:
            responseSample = {}
            for orderedColumn in order:

                formatted_ordered_col = orderedColumn[0].lower() + orderedColumn[1:]
                try:
                    dataFieldName = columnFeatures[orderedColumn]["data"]
                    if formatted_ordered_col in sample:
                        orderedSample = sample[formatted_ordered_col]

                        if orderedColumn == "IgoQcRecommendation":

                            recommendation = sample[
                                orderedColumn[0].lower() + orderedColumn[1:]
                            ].lower()
                            responseSample[dataFieldName] = "<div class=%s>%s</div>" % (
                                recommendation,
                                orderedSample,
                            )
                        elif (
                            orderedColumn == "Concentration"
                            or orderedColumn == "TotalMass"
                            or orderedColumn == "Rin"
                            or orderedColumn == "Din"
                            or orderedColumn == "DV200"
                        ):
                            if orderedSample:
                                responseSample[dataFieldName] = round(
                                    float(orderedSample), 1
                                )
                        elif orderedColumn == "Volume" or orderedColumn == "AvgSize":
                            if orderedSample:
                                responseSample[dataFieldName] = round(
                                    float(orderedSample), 0
                                )

                        elif orderedColumn == "Action":

                            responseSample[dataFieldName] = (
                                "<span class ='download-icon'><i class=%s>%s</i></span>"
                                % ("material-icons", "cloud_download")
                            )
                        elif orderedColumn == "SampleStatus":
                            responseSample[dataFieldName] = "<div class=%s>%s</div>" % (
                                'pathology-status',
                                orderedSample,
                            )
                        elif orderedColumn == "InvestigatorDecision":
                            # print(sample)
                            if dataFieldName in sample:
                                responseSample[dataFieldName] = orderedSample
                            else:
                                responseSample[dataFieldName] = None
                        else:

                            responseSample[dataFieldName] = orderedSample

                    else:
                        if orderedColumn == "Action":

                            responseSample[dataFieldName] = (
                                "<span class ='download-icon'><i class=%s>%s</i></span>"
                                % ("material-icons", "cloud_download")
                            )
                        else:
                            responseSample[dataFieldName] = ""
                except:
                    print(traceback.print_exc())
                    print(sample)
                    # Excpected column not found in LIMS result, return it to FE anyway.
                    responseSample[dataFieldName] = ""
            responseSamples.append(responseSample)

        return {
            "data": responseSamples,
            "columnFeatures": responseColumns,
            "columnHeaders": responseHeaders,
        }


def build_pending_list(pendings):

    responsePendings = []

    for pending in pendings:
        responsePending = {}
        responsePending["request_id"] = pending.request_id
        responsePending["date"] = pending.date_created
        responsePending["report"] = pending.report
        responsePending["author"] = pending.author
        responsePending["recipients"] = (
            "<div class='recipients-col'>"
            + pending.recipients.replace(',', ',\n')
            + "</div>"
        )
        responsePending["show"] = (
            "<span class ='show-icon'><i class=%s>%s</i></span>"
            % ("material-icons", "forward")
        )

        responsePendings.append(responsePending)

    return {
        "data": responsePendings,
        "columnFeatures": [
            {"data": "request_id", "readOnly": "true"},
            {"data": "date", "readOnly": "true"},
            {"data": "report", "readOnly": "true"},
            {"data": "author", "readOnly": "true"},
            {"data": "recipients", "readOnly": "true", "renderer": "html"},
            {"data": "show", "readOnly": "true", "renderer": "html"},
            # last column will be hidden in FE
            # {"data": "recordId", "readOnly": "true"},
        ],
        "columnHeaders": constants.pending_order,
    }


def build_attachment_list(field, attachments):

    responseAttachments = []

    for attachment in attachments:
        responseAttachment = {}
        responseAttachment["fileName"] = attachment["fileName"]
        responseAttachment["recordId"] = attachment["recordId"]
        responseAttachment["action"] = "Download " + str(attachment["recordId"])
        responseAttachments.append(responseAttachment)

    return {
        "data": responseAttachments,
        "columnFeatures": [
            {"data": "fileName", "readOnly": "true"},
            {"data": "action", "readOnly": "true"},
            # last column will be hidden in FE
            {"data": "recordId", "readOnly": "true"},
        ],
        "columnHeaders": ["File Name", "Action", "RecordId"],
    }


def get_picklist(listname):

    if uwsgi.cache_exists(listname):
        return pickle.loads(uwsgi.cache_get(listname))
    else:

        r = s.get(
            LIMS_API_ROOT + "/getPickListValues?list=%s" % listname,
            auth=(LIMS_USER, LIMS_PW),
            verify=False,
        )
        picklist = []
        for value in json.loads(r.content.decode('utf-8')):
            picklist.append(value)
        uwsgi.cache_set(listname, pickle.dumps(picklist), 900)
        return pickle.loads(uwsgi.cache_get(listname))
    # return picklist


def tmp_file_exists(file_name):
    return os.path.exists(TMP_FOLDER + file_name)


def log_info(message):
    print(message)


# returns true if user is associated with request as recipient
# returns false if request has no inital comment OR user is not associated
def is_user_authorized_for_request(request_id, username):
    commentrelations = CommentRelation.query.filter_by(request_id=request_id)
    for relation in commentrelations:
        if username in relation.recipients:
            return True
    return False


def save_decision(decisions, request_id, username):
    try:
        user = User.query.filter_by(username=username).first()

        decision_to_save = Decision(
            decisions=json.dumps(decisions),
            request_id=request_id,
            date_created=datetime.now(),
            date_updated=datetime.now(),
        )

        user.decisions.append(decision_to_save)

        db.session.commit()
        return decision_to_save
    except:
        print(traceback.print_exc())

        return None

    return None


def send_decision_notification(decision, decision_user, recipients):
    receiver_email = "wagnerl@mskcc.org,patrunoa@mskcc.org"
    # receiver_email = recipients
    sender_email = NOTIFICATION_SENDER
    # print(receiver_email.split(","))

    template = constants.decision_notification_email_template_html

    content = (
        template["body"] % (decision.request_id, decision_user.full_name)
        + template["footer"]
        + "<br><br>In production, this email would have been sent to:"
        + ", ".join(recipients)
    )
    msg = MIMEText(content, "html")
    msg['Subject'] = template["subject"] % decision.request_id

    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    # .sendmail(sender_email, receiver_email, message.as_string())
    # if ENV = development
    s.sendmail(sender_email, receiver_email.split(","), msg.as_string())
    s.close()
    print(msg.as_string())
    return "done"

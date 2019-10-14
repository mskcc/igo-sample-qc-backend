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


import sys
import re
import copy
from app import app, constants
import os.path
import uwsgi, pickle
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
import pandas as pd
from io import BytesIO

from openpyxl.writer.excel import save_virtual_workbook

# MORE IMPORTANT THAN IT SHOULD BE
app.config['JSON_SORT_KEYS'] = False
# _________________________________

LIMS_API_ROOT = app.config["LIMS_API_ROOT"]
LIMS_USER = app.config["LIMS_USER"]
LIMS_PW = app.config["LIMS_PW"]
TMP_FOLDER = app.config["TMP_FOLDER"]

# LIMS_REST_API_ROOT = app.config["LIMS_REST_API_ROOT"]
# LIMS_API_USER = app.config["LIMS_API_USER"]
# LIMS_API_PW = app.config["LIMS_API_PW"]
# LIMS_GUID = app.config["LIMS_GUID"]

qc_report = Blueprint("qc_report", __name__)


# request = package.session
s = requests.Session()
# lims_headers = {'guid': LIMS_GUID}
# s.mount("https://", MyAdapter())


# returns request level information including a list of samples in the request
# queries IGO LIMS REST
@qc_report.route("/getRequestSamples", methods=['GET'])
def get_request_samples():
    return_text = ""

    request_id = request.args.get("request_id")

    # the API endpoint
    r = s.get(
        LIMS_API_ROOT + "/api/getRequestSamples?request=" + request_id,
        auth=(LIMS_USER, LIMS_PW),
        verify=False,
    )
    # print(r)
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
            responseData["request"]["investigatorName"] = lims_data["investigatorName"]
            responseData["request"]["dataAnalystName"] = lims_data["dataAnalystName"]
            responseData["request"]["projectManagerName"] = lims_data[
                "projectManagerName"
            ]

            responseData["recipients"]["IGOEmail"] = "zzPDL_CMO_IGO@mskcc.org"
            responseData["recipients"]["LabHeadEmail"] = lims_data["labHeadEmail"]
            responseData["recipients"]["InvestigatorEmail"] = lims_data[
                "investigatorEmail"
            ]
            responseData["recipients"]["DataAnalystEmail"] = lims_data[
                "dataAnalystEmail"
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
            return make_response("Request not found", 404, None)
    else:

        response = make_response(r.text, r.status_code, None)
        return response

    response = make_response(return_text, 200, None)
    return response


# queries SAPIO LIMS REST
@qc_report.route("/getQcReportSamples", methods=["POST"])
def get_qc_report_samples():
    # makes an empty dictionary
    data = dict()
    # gets payload
    payload = request.get_json()["data"]
    # parses payload into params
    # print(payload)
    request_id = payload["request"]
    samples = payload["samples"]
    # puts the params in the dictionary
    data['request'] = request_id
    data['samples'] = samples

    # params =

    # calls API endpoint and passes in necessary params

    # r = s.get(
    #        LIMS_REST_API_ROOT + "/datarecord",
    #        headers=headers,
    #        auth=(LIMS_API_USER, LIMS_API_PW),
    #        data={
    #            "datatype": "QcReportDna",
    #            "field": "OtherSampleId",
    #            "values": [AdCCDK_1T, AdCCDK_7T, AdCCHW],
    #        },
    #        verify=False,
    #    )

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
        # print(lims_data)
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
    payload = request.get_json()["data"]

    r = s.post(
        LIMS_API_ROOT + "/setQcInvestigatorDecision",
        auth=(LIMS_USER, LIMS_PW),
        verify=False,
        data=json.dumps(payload),
    )

    return r.text


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
                print("Unexpected error:%s" % (sys.exc_info()[0]))

                try:
                    # delete field from sample if we don't expect it in the FE
                    for sample in responseSamples:
                        sample.pop(orderedColumn)
                except:
                    #
                    # if sample.pop failed, excpected column not found in LIMS result, return it to FE anyway.
                    responseColumns[orderedColumn] = {}
                    responseHeaders.append(
                        columnFeatures[orderedColumn]["columnHeader"]
                    )

        for sample in samples:
            responseSample = {}
            for orderedColumn in order:
                try:

                    if orderedColumn == "IgoQcRecommendation":
                        recommendation = sample[
                            orderedColumn[0].lower() + orderedColumn[1:]
                        ].lower()
                        responseSample[columnFeatures[orderedColumn]["data"]] = (
                            "<div class=%s>%s</div>"
                            % (
                                recommendation,
                                sample[orderedColumn[0].lower() + orderedColumn[1:]],
                            )
                        )
                    elif orderedColumn == "Action":

                        responseSample[columnFeatures[orderedColumn]["data"]] = (
                            "<span class ='download-icon'><i class=%s>%s</i></span>"
                            % ("material-icons", "cloud_download")
                        )
                    elif orderedColumn == "InvestigatorDecision":
                        # print(sample)
                        if columnFeatures[orderedColumn]["data"] in sample:
                            responseSample[
                                columnFeatures[orderedColumn]["data"]
                            ] = sample[orderedColumn[0].lower() + orderedColumn[1:]]
                        else:
                            responseSample[columnFeatures[orderedColumn]["data"]] = None
                    else:
                        responseSample[columnFeatures[orderedColumn]["data"]] = sample[
                            orderedColumn[0].lower() + orderedColumn[1:]
                        ]
                except:
                    # Excpected column not found in LIMS result, return it to FE anyway.
                    responseSample[columnFeatures[orderedColumn]["data"]] = ""
            responseSamples.append(responseSample)

        return {
            "data": responseSamples,
            "columnFeatures": responseColumns,
            "columnHeaders": responseHeaders,
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

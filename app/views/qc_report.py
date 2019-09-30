from flask import Flask, Blueprint, json, jsonify, request, make_response
import requests
import sys
import copy
from app import app, constants

# MORE IMPORTANT THAN IT SHOULD BE
app.config['JSON_SORT_KEYS'] = False
# _________________________________

LIMS_API_ROOT = app.config["LIMS_API_ROOT"]
LIMS_USER = app.config["LIMS_USER"]
LIMS_PW = app.config["LIMS_PW"]

LIMS_REST_API_ROOT = app.config["LIMS_REST_API_ROOT"]
LIMS_API_USER = app.config["LIMS_API_USER"]
LIMS_API_PW = app.config["LIMS_API_PW"]
LIMS_GUID = app.config["LIMS_GUID"]

qc_report = Blueprint("qc_report", __name__)


# request = package.session
s = requests.Session()
lims_headers = {'guid': LIMS_GUID}
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
        # print(lims_data)
        responseData = {}

        if "samples" in lims_data:
            responseData["requestId"] = lims_data["requestId"]
            responseData["labHeadName"] = lims_data["labHeadName"]
            responseData["investigatorName"] = lims_data["investigatorName"]
            responseData["dataAnalystName"] = lims_data["dataAnalystName"]
            responseData["projectManagerName"] = lims_data["projectManagerName"]
            responseData["samples"] = []
            # we only need Investigator Sample Ids
            for sample in lims_data["samples"]:
                responseData["samples"].append(sample["investigatorSampleId"])

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

    # request_id = payload["request"]
    # samples = payload["samples"]
    # puts the params in the dictionary
    # data['request'] = request_id
    # print(payload)
    r = s.post(
        LIMS_API_ROOT + "/setQcInvestigatorDecision",
        auth=(LIMS_USER, LIMS_PW),
        verify=False,
        data=json.dumps(payload),
    )

    # r = s.get(
    #     LIMS_REST_API_ROOT + "/attachment",
    #     headers=lims_headers,
    #     auth=(LIMS_API_USER, LIMS_API_PW),
    #     params={"datatype": "Attachment", "fields": {"CreatedBy": "chend"}},
    #     verify=False,
    # )
    # print(r)

    return "200"


@qc_report.route("/getAttachments", methods=["GET"])
def get_qc_report_attachments():
    r = s.get(
        LIMS_REST_API_ROOT + "/attachment",
        headers=lims_headers,
        auth=(LIMS_API_USER, LIMS_API_PW),
        params={"datatype": "Attachment", "fields": {"recordId": "5972466"}},
        verify=False,
    )
    # print(r)

    return r.text


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

                    #     print(columnFeatures[orderedColumn])
                    #     responseColumns[orderedColumn]["source"] = get_picklist(
                    #         columnFeatures[orderedColumn]["picklistName"]
                    #     )
                    #     print(get_picklist(columnFeatures[orderedColumn]["picklistName"]))

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
                    elif orderedColumn == "InvestigatorDecision":
                        print(sample)
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


def get_picklist(listname):
    # if uwsgi.cache_exists(listname):
    #     return pickle.loads(uwsgi.cache_get(listname))
    # else:

    r = s.get(
        LIMS_API_ROOT + "/getPickListValues?list=%s" % listname,
        auth=(LIMS_USER, LIMS_PW),
        verify=False,
    )
    picklist = []
    for value in json.loads(r.content.decode('utf-8')):
        picklist.append(value)
    # uwsgi.cache_set(listname, pickle.dumps(picklist), 900)
    # return pickle.loads(uwsgi.cache_get(listname))
    return picklist

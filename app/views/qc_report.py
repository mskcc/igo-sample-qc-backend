from flask import Flask, Blueprint, json, jsonify, request, make_response
import requests
import copy
from app import app, constants


LIMS_API_ROOT = app.config["LIMS_API_ROOT"]
LIMS_USER = app.config["LIMS_USER"]
LIMS_PW = app.config["LIMS_PW"]

qc_report = Blueprint("qc_report", __name__)


# request = package.session
s = requests.Session()
# s.mount("https://", MyAdapter())


# returns request level information including a list of samples in the request
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
    print(r)
    if r.status_code == 200:
        return_text += r.text
    else:

        response = make_response(r.text, r.status_code, None)
        return response

    response = make_response(return_text, 200, None)
    return response


# add a new POST route /getQcReportSamples that
@qc_report.route("/getQcReportSamples", methods=["POST"])
def get_qc_report_samples():
    # makes an empty dictionary
    data = dict()
    # gets payload
    payload = request.get_json()["data"]
    # parses payload into params
    request_id = payload["request"]
    samples = payload["samples"]
    # puts the params in the dictionary
    data['request'] = request_id
    data['samples'] = samples

    # calls API endpoint and passes in necessary params
    r = s.post(
        LIMS_API_ROOT + "/getQcReportSamples",
        auth=(LIMS_USER, LIMS_PW),
        verify=False,
        data=data,
    )
    # print(constants.allColumns)
    return_text = ""
    if r.status_code == 200:
        # assemble table data
        lims_data = r.json()
        tables = dict()
        for field in lims_data:
           
            if field == "dnaReportSamples":
                columnFeatures = Merge(constants.sharedColumns, constants.dnaColumns)
                tables[field] = build_table(field, lims_data[field], columnFeatures)

            if field == "rnaReportSamples":
                columnFeatures = Merge(constants.sharedColumns, constants.rnaColumns)
                tables[field] = build_table(field, lims_data[field], columnFeatures)
            if field == "libraryReportSamples":
                columnFeatures = Merge(
                    constants.sharedColumns, constants.libraryColumns
                )
                tables[field] = build_table(field, lims_data[field], columnFeatures)
        # print(tables)

        return jsonify(tables)
    else:
  
        response = make_response(r.text, r.status_code, None)
        return response


    response = make_response(return_text)
    return response


# -------------UTIL-------------
# Python code to merge dict using a single
# expression
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def build_table(reportTable, samples, columnFeatures):
    responseColumns = dict()
    responseSamples = copy.deepcopy(samples)
    for column in samples[0]:
        try:
            responseColumns[column] = columnFeatures[column]
        except:
            print(column + " not found in expected columns for " + reportTable)
            for sample in responseSamples:
                sample.pop(column)

    return {"data": responseSamples, "columnFeatures": responseColumns}

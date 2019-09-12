from flask import Flask, Blueprint, json, jsonify, request, make_response
import requests
from app import app


LIMS_API_ROOT = app.config["LIMS_API_ROOT"]
LIMS_USER = app.config["LIMS_USER"]
LIMS_PW = app.config["LIMS_PW"]

qc_report = Blueprint("qc_report", __name__)


# request = package.session
s = requests.Session()
# s.mount("https://", MyAdapter())

# three tables that will need to be connected in an endpoint? qcreportrna, dna, library
# suggestion: controller - getqc_report(request_id), service - getqc_report
@qc_report.route("/qc_report/rna")
def qc_report_rna():
    # the API endpoint
    r = s.get(
        # LIMS_API_ROOT + "/LimsRest/getProjectQc?project='09938'",
        LIMS_API_ROOT + "/LimsRest/getPickListValues?list=Recipe",
        auth=(LIMS_USER, LIMS_PW),
        verify=False,
    )
    print(r.text)
    # return "rna-result";
    return r.text


# add a new POST route /getQcReportSamples that
@qc_report.route("/getQcReportSamples", methods=["POST"])
def get_qc_report_samples():
    # makes an empty dictionary
    data = dict()   
    # gets payload
    payload = request.get_json()
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
    # print(r)
    return r.text
